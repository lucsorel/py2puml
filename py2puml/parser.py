from typing import Iterable, Type, List, Dict
from types import ModuleType
from enum import Enum
from inspect import getmembers, isclass
from re import compile

from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlclass import UmlClass, UmlAttribute
from py2puml.domain.umlenum import UmlEnum, Member
from py2puml.domain.umlrelation import UmlRelation, RelType
from py2puml.utils import inspect_type

CONCRETE_TYPE_PATTERN = compile("^<(?:class|enum) '([\\.|\\w]+)'>$")
def filter_domain_definitions(module: ModuleType, root_module_name: str) -> Iterable[Type]:
    for definition_key in dir(module):
        definition_type = getattr(module, definition_key)
        if isclass(definition_type):
            definition_members = getmembers(definition_type)
            definition_module_member = next((
                member for member in definition_members
                # ensures that the type belongs to the module being parsed
                if member[0] == '__module__' and member[1].startswith(root_module_name)
            ), None)
            if definition_module_member is not None:
                yield definition_type

def get_type_name(type: Type, root_module_name: str):
    if type.__module__.startswith(root_module_name):
        return type.__name__
    else:
        return f'{type.__module__}.{type.__name__}'

def parse_enum_type(
    enum_type: Type,
    enum_type_fqdn: str,
    domain_items_by_fqdn: Dict[str, UmlItem]
):
    domain_items_by_fqdn[enum_type_fqdn] = UmlEnum(
        name=enum_type.__name__,
        fqdn=enum_type_fqdn,
        members=[
            Member(name=enum_member.name, value=enum_member.value)
            for enum_member in enum_type.__members__.values()
        ]
    )

def parse_namedtupled_class(
    namedtupled_type: Type,
    namedtupled_type_fqdn: str,
    domain_items_by_fqdn: Dict[str, UmlItem]
):
    domain_items_by_fqdn[namedtupled_type_fqdn] = UmlClass(
        name=namedtupled_type.__name__,
        fqdn=namedtupled_type_fqdn,
        attributes=[
            UmlAttribute(tuple_field, 'any')
            for tuple_field in namedtupled_type._fields
        ]
    )


def handle_inheritance_relation(
    class_type: Type,
    class_fqdn: str,
    root_module_name: str,
    domain_relations: List[UmlRelation]
):
    for base_type in getattr(class_type, '__bases__', ()):
        base_type_fqdn = f'{base_type.__module__}.{base_type.__name__}'
        if base_type_fqdn.startswith(root_module_name):
            domain_relations.append(
                UmlRelation(base_type_fqdn, class_fqdn, RelType.INHERITANCE)
            )

def parse_class_type(
    class_type: Type,
    class_type_fqdn: str,
    root_module_name: str,
    domain_items_by_fqdn: Dict[str, UmlItem],
    domain_relations: List[UmlRelation]
):
    definition_attrs = []
    uml_class = UmlClass(
        name=class_type.__name__,
        fqdn=class_type_fqdn,
        attributes=definition_attrs
    )
    domain_items_by_fqdn[class_type_fqdn] = uml_class
    # inspect_type(class_type)
    type_annotations = getattr(class_type, '__annotations__', None)
    if type_annotations is not None:
        for attr_name, attr_class in type_annotations.items():
            attr_raw_type = str(attr_class)
            concrete_type_match = CONCRETE_TYPE_PATTERN.search(attr_raw_type)
            if concrete_type_match:
                concrete_type = concrete_type_match.group(1)
                if attr_class.__module__.startswith(root_module_name):
                    attr_type = attr_class.__name__
                    domain_relations.append(
                        UmlRelation(uml_class.fqdn, f'{attr_class.__module__}.{attr_class.__name__}', RelType.COMPOSITION)
                    )
                else:
                    attr_type = concrete_type
            else:
                composition_rel = getattr(attr_class, '_name', None)
                component_classes = getattr(attr_class, '__args__', None)
                if composition_rel and component_classes:
                    component_names = [
                        get_type_name(component_class, root_module_name)
                        for component_class in component_classes
                        # filters out forward refs
                        if getattr(component_class, '__name__', None) is not None
                    ]
                    domain_relations.extend([
                        UmlRelation(uml_class.fqdn, f'{component_class.__module__}.{component_class.__name__}', RelType.COMPOSITION)
                        for component_class in component_classes
                        if component_class.__module__.startswith(root_module_name)
                    ])
                    attr_type = f"{composition_rel}[{', '.join(component_names)}]"
                else:
                    attr_type = attr_raw_type
            uml_attr = UmlAttribute(attr_name, attr_type)
            definition_attrs.append(uml_attr)

    handle_inheritance_relation(class_type, class_type_fqdn, root_module_name, domain_relations)


def parse_type(
    definition_type: Type,
    root_module_name: str,
    domain_items_by_fqdn: Dict[str, UmlItem],
    domain_relations: List[UmlRelation]
):
    definition_type_fqdn = f'{definition_type.__module__}.{definition_type.__name__}'
    if definition_type_fqdn not in domain_items_by_fqdn:
        if issubclass(definition_type, Enum):
            parse_enum_type(definition_type, definition_type_fqdn, domain_items_by_fqdn)
        elif getattr(definition_type, '_fields', None) is not None:
            parse_namedtupled_class(definition_type, definition_type_fqdn, domain_items_by_fqdn)
        else:
            parse_class_type(definition_type, definition_type_fqdn, root_module_name, domain_items_by_fqdn, domain_relations)


def parse_item_module(
    domain_item_module: ModuleType,
    root_module_name: str,
    domain_items_by_fqdn: Dict[str, UmlItem],
    domain_relations: List[UmlRelation]
):
    # processes only the classes imported and defined within the given root module
    for definition_type in filter_domain_definitions(domain_item_module, root_module_name):
        parse_type(definition_type, root_module_name, domain_items_by_fqdn, domain_relations)
