
from inspect import isabstract, signature
import inspect
from typing import Type, List, Dict

from re import compile
from dataclasses import dataclass

from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlclass import UmlClass, UmlAttribute, UmlMethod
from py2puml.domain.umlrelation import UmlRelation, RelType
from py2puml.parsing.parseclassconstructor import parse_class_constructor

CONCRETE_TYPE_PATTERN = compile("^<(?:class|enum) '([\\.|\\w]+)'>$")

def get_type_name(type: Type, root_module_name: str):
    if type.__module__.startswith(root_module_name):
        return type.__name__
    else:
        return f'{type.__module__}.{type.__name__}'

def handle_inheritance_relation(
    class_type: Type,
    class_fqn: str,
    root_module_name: str,
    domain_relations: List[UmlRelation]
):
    for base_type in getattr(class_type, '__bases__', ()):
        base_type_fqn = f'{base_type.__module__}.{base_type.__name__}'
        if base_type_fqn.startswith(root_module_name):
            domain_relations.append(
                UmlRelation(base_type_fqn, class_fqn, RelType.INHERITANCE)
            )

def inspect_static_attributes(
    class_type_fqn: str,
    definition_attrs: List[UmlAttribute],
    class_type: Type,
    root_module_name: str,
    domain_relations: List[UmlRelation]
):
    # inspect_domain_definition(class_type)
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
                        UmlRelation(class_type_fqn, f'{attr_class.__module__}.{attr_class.__name__}', RelType.COMPOSITION)
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
                        UmlRelation(class_type_fqn, f'{component_class.__module__}.{component_class.__name__}', RelType.COMPOSITION)
                        for component_class in component_classes
                        if component_class.__module__.startswith(root_module_name)
                    ])
                    attr_type = f"{composition_rel}[{', '.join(component_names)}]"
                else:
                    attr_type = attr_raw_type
            uml_attr = UmlAttribute(attr_name, attr_type, static=True)
            definition_attrs.append(uml_attr)


def inspect_methods(
    definition_methods, class_type,
):
    no_dunder = lambda x: not (x[0].startswith('__') or x[0].endswith('__'))
    methods = filter(no_dunder, inspect.getmembers(class_type, callable))
    for name, method in methods:
        signature = inspect.signature(method)
        uml_method = UmlMethod(
            name=name,
            signature=str(signature),
        )
        definition_methods.append(uml_method)


def handle_class_type(
    class_type: Type,
    class_type_fqn: str,
    domain_items_by_fqn: Dict[str, UmlItem],
) -> UmlClass:
    definition_attrs: List[UmlAttribute] = []
    definition_methods: List[UmlMethod] = []
    uml_class = UmlClass(
        name=class_type.__name__,
        fqn=class_type_fqn,
        attributes=definition_attrs,
        methods=definition_methods,
        is_abstract=isabstract(class_type)
    )
    domain_items_by_fqn[class_type_fqn] = uml_class
    return uml_class

def inspect_class_type(
    class_type: Type,
    class_type_fqn: str,
    root_module_name: str,
    domain_items_by_fqn: Dict[str, UmlItem],
    domain_relations: List[UmlRelation]
):
    uml_class = handle_class_type(class_type, class_type_fqn, domain_items_by_fqn)
    inspect_static_attributes(
        class_type_fqn, uml_class.attributes, class_type, root_module_name, domain_relations
    )
    inspect_methods(uml_class.methods, class_type)
    instance_attributes, compositions = parse_class_constructor(class_type, class_type_fqn, root_module_name)
    uml_class.attributes.extend(instance_attributes)
    domain_relations.extend(compositions.values())

    handle_inheritance_relation(class_type, class_type_fqn, root_module_name, domain_relations)

def inspect_dataclass_type(
    class_type: Type,
    class_type_fqn: str,
    root_module_name: str,
    domain_items_by_fqn: Dict[str, UmlItem],
    domain_relations: List[UmlRelation]
):
    uml_class = handle_class_type(class_type, class_type_fqn, domain_items_by_fqn)
    inspect_static_attributes(
        class_type_fqn, uml_class.attributes, class_type, root_module_name, domain_relations
    )
    inspect_methods(uml_class.methods, class_type)
    for attribute in uml_class.attributes:
        attribute.static = False

    handle_inheritance_relation(class_type, class_type_fqn, root_module_name, domain_relations)