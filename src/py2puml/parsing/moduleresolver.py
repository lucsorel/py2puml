from functools import reduce
from inspect import isclass
from types import ModuleType
from typing import Iterable, List, NamedTuple, Type


class NamespacedType(NamedTuple):
    """
    Information of a value type:
    - the module-prefixed type name
    - the short type name
    """

    full_namespace: str
    type_name: str


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


def search_in_module(namespaces: List[str], module: ModuleType):
    leaf_type: Type = reduce(search_in_module_or_builtins, namespaces, module)
    if leaf_type is None:
        return EMPTY_NAMESPACED_TYPE
    else:
        # https://bugs.python.org/issue34422#msg323772
        short_type = getattr(leaf_type, '__name__', getattr(leaf_type, '_name', None))
        return NamespacedType(f'{leaf_type.__module__}.{short_type}', short_type)


class ModuleResolver:
    """
    Given a module and a partially namespaced type name, returns a tuple of information about the type:
    - the full-namespaced type name, to draw relationships between types without ambiguity
    - the short type name, for display purposes

    Different approaches are combined to derive the type information:
    - when the partially namespaced type is found during AST parsing (class constructors)
    - when the partially namespaced type is found during class inspection (dataclasses, class static variables, named tuples, enums)

    The two approaches are a bit entangled for now, they could be separated a bit more for performance sake.
    """

    def __init__(self, module: ModuleType):
        self.module = module

    def __repr__(self) -> str:
        return f'ModuleResolver({self.module})'

    def resolve_full_namespace_type(self, partial_dotted_path: str) -> NamespacedType:
        """
        Returns a tuple of 2 strings:
        - the full namespaced type
        - the short named type
        """
        if partial_dotted_path is None:
            return EMPTY_NAMESPACED_TYPE

        # special case for Union types
        if partial_dotted_path == 'None':
            return NamespacedType('builtins.None', 'None')

        def string_repr(module_attribute) -> str:
            return (
                f'{module_attribute.__module__}.{module_attribute.__name__}'
                if isclass(module_attribute)
                else f'{module_attribute}'
            )

        # searches the class in the module imports
        namespaced_types_iter: Iterable[NamespacedType] = (
            NamespacedType(string_repr(getattr(self.module, module_var)), module_var)
            for module_var in vars(self.module)
        )
        found_namespaced_type = next(
            (
                namespaced_type
                for namespaced_type in namespaced_types_iter
                if namespaced_type.full_namespace == partial_dotted_path
            ),
            None,
        )

        # searches the class in the builtins
        if found_namespaced_type is None:
            found_namespaced_type = search_in_module(partial_dotted_path.split('.'), self.module)

        return found_namespaced_type

    def get_module_full_name(self) -> str:
        return self.module.__name__
