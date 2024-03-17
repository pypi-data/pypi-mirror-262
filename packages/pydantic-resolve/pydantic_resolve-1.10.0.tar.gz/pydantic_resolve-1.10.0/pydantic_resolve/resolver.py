import asyncio
import contextvars
import inspect
import warnings
from inspect import iscoroutine
from collections import defaultdict
from typing import TypeVar, Dict
from .exceptions import MissingAnnotationError
from typing import Any, Optional
from pydantic_resolve import core
from aiodataloader import DataLoader
from types import MappingProxyType
import pydantic_resolve.constant as const
import pydantic_resolve.util as util


T = TypeVar("T")

class Resolver:
    def __init__(
            self,
            loader_filters: Optional[Dict[Any, Dict[str, Any]]] = None,  # deprecated
            loader_params: Optional[Dict[Any, Dict[str, Any]]] = None,
            global_loader_filter: Optional[Dict[str, Any]] = None,  # deprecated
            global_loader_param: Optional[Dict[str, Any]] = None,
            loader_instances: Optional[Dict[Any, Any]] = None,
            ensure_type=False,
            context: Optional[Dict[str, Any]] = None):
        self.loader_instance_cache = {}

        self.ancestor_vars = {}
        self.collector_contextvars = {}

        # for dataloader which has class attributes, you can assign the value at here
        if loader_filters:
            warnings.warn('loader_filters is deprecated, use loader_params instead.', DeprecationWarning)
            self.loader_params = loader_filters
        else:
            self.loader_params = loader_params or {}

        # keys in global_loader_filter are mutually exclusive with key-value pairs in loader_filters
        # eg: Resolver(global_loader_filter={'key_a': 1}, loader_filters={'key_a': 1}) will raise exception
        if global_loader_filter:
            warnings.warn('global_loader_filter is deprecated, use global_loader_param instead.', DeprecationWarning)
            self.global_loader_param = global_loader_filter or {}
        else:
            self.global_loader_param = global_loader_param or {}

        # now you can pass your loader instance, Resolver will check `isinstance``
        if loader_instances and self._validate_loader_instance(loader_instances):
            self.loader_instances = loader_instances
        else:
            self.loader_instances = {}

        self.ensure_type = ensure_type
        self.context = MappingProxyType(context) if context else None
        self.metadata = {}

    def _validate_loader_instance(self, loader_instances: Dict[Any, Any]):
        for cls, loader in loader_instances.items():
            if not issubclass(cls, DataLoader):
                raise AttributeError(f'{cls.__name__} must be subclass of DataLoader')
            if not isinstance(loader, cls):
                raise AttributeError(f'{loader.__name__} is not instance of {cls.__name__}')
        return True
    
    def _prepare_collectors(self, target):
        for alias, collector_instance, sign in core.get_collectors(target, self.metadata):
            if not self.collector_contextvars.get(alias):
                self.collector_contextvars[alias] = {}

            if sign not in self.collector_contextvars[alias]:
                self.collector_contextvars[alias][sign] = contextvars.ContextVar('-'.join(sign))

            self.collector_contextvars[alias][sign].set(collector_instance)

    def _add_values_into_collectors(self, target):
        for field, alias in core.iter_over_collectable_fields(target, self.metadata):
            for _, instance_ctx in self.collector_contextvars[alias].items():
                collector = instance_ctx.get()
                val = getattr(target, field)
                collector.add(val)

    def _add_expose_fields(self, target):
        expose_dict: Optional[dict] = getattr(target, const.EXPOSE_TO_DESCENDANT, None)
        if expose_dict:
            for field, alias in expose_dict.items():  # eg: {'name': 'bar_name'}
                if not self.ancestor_vars.get(alias):
                    self.ancestor_vars[alias] = contextvars.ContextVar(alias)

                try:
                    val = getattr(target, field)
                except AttributeError:
                    raise AttributeError(f'{field} does not existed')

                self.ancestor_vars[alias].set(val)

    def _prepare_ancestor_context(self):
        return {k: v.get() for k, v in self.ancestor_vars.items()}

    def _execute_resolver_method(self, method):
        signature = inspect.signature(method)
        params = {}

        if signature.parameters.get('context'):
            if self.context is None:
                raise AttributeError('Resolver.context is missing')
            params['context'] = self.context

        if signature.parameters.get('ancestor_context'):
            if self.ancestor_vars is None:
                raise AttributeError(f'there is not class has {const.EXPOSE_TO_DESCENDANT} configed')
            params['ancestor_context'] = self._prepare_ancestor_context()

        for k, v in signature.parameters.items():
            if isinstance(v.default, core.Depends):
                cache_key = util.get_kls_full_path(v.default.dependency)
                loader = self.loader_instance_cache[cache_key]
                params[k] = loader

        return method(**params)

    def _execute_post_method(self, method):
        signature = inspect.signature(method)
        params = {}

        if signature.parameters.get('context'):
            if self.context is None:
                raise AttributeError('Post.context is missing')
            params['context'] = self.context

        if signature.parameters.get('ancestor_context'):
            if self.ancestor_vars is None:
                raise AttributeError(f'there is not class has {const.EXPOSE_TO_DESCENDANT} configed')
            params['ancestor_context'] = self._prepare_ancestor_context()

        ret_val = method(**params)
        return ret_val
    
    async def _resolve_obj_field(self, target, field, trim_field, attr):
        if self.ensure_type:
            if not attr.__annotations__:
                raise MissingAnnotationError(f'{field}: return annotation is required')

        val = self._execute_resolver_method(attr)
        while iscoroutine(val) or asyncio.isfuture(val):
            val = await val

        if not getattr(attr, const.HAS_MAPPER_FUNCTION, False):  # defined in util.mapper
            val = util.try_parse_data_to_target_field_type(target, trim_field, val)

        # continue dive deeper
        val = await self._resolve(val)

        setattr(target, trim_field, val)

    async def _resolve(self, target: T) -> T:
        if isinstance(target, (list, tuple)):
            await asyncio.gather(*[self._resolve(t) for t in target])

        if core.is_acceptable_instance(target):
            self._prepare_collectors(target)
            self._add_expose_fields(target)

            tasks = []

            # traversal and fetching data by resolve methods
            resolve_list, attribute_list = core.iter_over_object_resolvers_and_acceptable_fields(target, self.metadata)
            for field, resolve_trim_field, method in resolve_list:
                tasks.append(self._resolve_obj_field(target, field, resolve_trim_field, method))
            for field, attr_object in attribute_list:
                tasks.append(self._resolve(attr_object))
            await asyncio.gather(*tasks)

            # reverse traversal and run post methods
            for post_key, post_trim_field in core.iter_over_object_post_methods(target, self.metadata):
                post_method = getattr(target, post_key)
                result = self._execute_post_method(post_method)
                result = util.try_parse_data_to_target_field_type(target, post_trim_field, result)
                setattr(target, post_trim_field, result)

            default_post_method = getattr(target, const.POST_DEFAULT_HANDLER, None)
            if default_post_method:
                self._execute_post_method(default_post_method)

            # collect after all done
            self._add_values_into_collectors(target)

        return target

    async def resolve(self, target: T) -> T:
        if isinstance(target, list) and target == []: return target

        root_class = core.get_class(target)
        self.metadata = core.scan_and_store_metadata(root_class)
        self.loader_instance_cache = core.validate_and_create_loader_instance(
            self.loader_params,
            self.global_loader_param,
            self.loader_instances,
            self.metadata)
            
        await self._resolve(target)
        return target
