from dataclasses import is_dataclass
from enum import Enum
from inspect import getmembers, isclass
from types import ModuleType
from typing import Dict, Iterable, List, Type

from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlrelation import UmlRelation
from py2puml.inspection.inspectclass import inspect_class_type, inspect_dataclass_type
from py2puml.inspection.inspectenum import inspect_enum_type
from py2puml.inspection.inspectnamedtuple import inspect_namedtuple_type


def filter_domain_definitions(module: ModuleType, root_module_name: str) -> Iterable[Type]:
    for definition_key in dir(module):
        definition_type = getattr(module, definition_key)
        if isclass(definition_type):
            definition_members = getmembers(definition_type)
            definition_module_member = next(
                (
                    member
                    for member in definition_members
                    # ensures that the type belongs to the module being parsed
                    if member[0] == '__module__' and member[1].startswith(root_module_name)
                ),
                None,
            )
            if definition_module_member is not None:
                yield definition_type


def inspect_domain_definition(
    definition_type: Type,
    root_module_name: str,
    domain_items_by_fqn: Dict[str, UmlItem],
    domain_relations: List[UmlRelation],
):
    definition_type_fqn = f'{definition_type.__module__}.{definition_type.__name__}'
    if definition_type_fqn not in domain_items_by_fqn:
        if issubclass(definition_type, Enum):
            inspect_enum_type(definition_type, definition_type_fqn, domain_items_by_fqn)
        elif getattr(definition_type, '_fields', None) is not None:
            inspect_namedtuple_type(definition_type, definition_type_fqn, domain_items_by_fqn)
        elif is_dataclass(definition_type):
            inspect_dataclass_type(
                definition_type, definition_type_fqn, root_module_name, domain_items_by_fqn, domain_relations
            )
        else:
            inspect_class_type(
                definition_type, definition_type_fqn, root_module_name, domain_items_by_fqn, domain_relations
            )


def inspect_module(
    domain_item_module: ModuleType,
    root_module_name: str,
    domain_items_by_fqn: Dict[str, UmlItem],
    domain_relations: List[UmlRelation],
):
    # processes only the definitions declared or imported within the given root module
    for definition_type in filter_domain_definitions(domain_item_module, root_module_name):
        inspect_domain_definition(definition_type, root_module_name, domain_items_by_fqn, domain_relations)
