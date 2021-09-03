
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
        - the full namespaced type
        - the short named type
        '''
        if partial_dotted_path is None:
            return EMPTY_NAMESPACED_TYPE
        
        namespaces = partial_dotted_path.split('.')
        leaf_type: Type = reduce(
            search_in_module_or_builtins,
            namespaces,
            self.module
        )
        if leaf_type is None:
            return EMPTY_NAMESPACED_TYPE
        else:
            # https://bugs.python.org/issue34422#msg323772
            short_type = getattr(leaf_type, '__name__', getattr(leaf_type, '_name', None))
            return NamespacedType(
                f'{leaf_type.__module__}.{short_type}',
                short_type
            )

    def get_module_full_name(self) -> str:
        return self.module.__name__
