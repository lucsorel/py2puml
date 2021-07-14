
from typing import Type, Tuple
from types import ModuleType
from collections import namedtuple

from functools import reduce

NamespacedType = namedtuple('NamespacedType', ['full_namespace', 'type_name'])

EMPTY_NAMESPACED_TYPE = NamespacedType(None, None)

def search_in_module_or_builtins(searched_module: ModuleType, namespace: str):
    if searched_module is None:
        return None

    # searches the namespace in the module definitions and imports
    found_module_or_leaf_type = getattr(searched_module, namespace, None)
    if found_module_or_leaf_type is not None:
        return found_module_or_leaf_type

    # searches the namespace in the builtins otherwise
    if hasattr(searched_module, '__builtins__'):
        return searched_module.__builtins__.get(namespace, None)
    else:
        return None

class ModuleResolver(object):
    def __init__(self, module: ModuleType):
        self.module = module

    def resolve_full_namespace_type(self, partial_dotted_path: str) -> Tuple[str, str]:
        '''
        Returns a tuple of 2 strings:
        - the full namespaced
        '''
        if partial_dotted_path is None:
            return EMPTY_NAMESPACED_TYPE
        
        namespaces = partial_dotted_path.split('.')
        leaf_type: Type = reduce(
            search_in_module_or_builtins,
            # lambda searched_module, namespace: None if searched_module is None else getattr(searched_module, namespace, None),
            namespaces,
            self.module
        )
        if leaf_type is None:
            return EMPTY_NAMESPACED_TYPE
        else:
            return NamespacedType(
                f'{leaf_type.__module__}.{leaf_type.__name__}',
                leaf_type.__name__
            )

    def get_module_full_name(self) -> str:
        return self.module.__name__
