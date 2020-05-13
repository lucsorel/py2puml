from typing import Iterable, Type, List, Dict
from types import ModuleType
from inspect import getmembers
from re import compile

from py2puml.domain.umlclass import UmlClass
from py2puml.domain.umlattribute import UmlAttribute
from py2puml.domain.umlcomposition import UmlComposition

CONCRETE_TYPE_PATTERN = compile("^<class '([\\.|\\w]+)'>$")

def filter_domain_definitions(module: ModuleType, root_module_name: str) -> Iterable[Type]:
    for definition_key in dir(module):
        definition_type = getattr(module, definition_key)
        definition_members = getmembers(definition_type)
        definition_module_member = next(
            (member for member in definition_members if member[0] == '__module__' and member[1].startswith(root_module_name)),
            None
        )
        if definition_module_member is not None:
            yield definition_type


def inspect_type(type: Type):
    '''
    Utilitary function which inspects the annotations of the given type
    '''
    type_annotations = getattr(type, '__annotations__', None)
    if type_annotations is None:
        print(f'class {type.__module__}.{type.__name__} has no annotation')
    else:
        # print(type.__annotations__)
        for attr_name, attr_class in type_annotations.items():
            for attr_class_key in dir(attr_class):
                if attr_class_key != '__doc__':
                    print(
                        f'{type.__name__}.{attr_name}:',
                        attr_class_key, getattr(attr_class, attr_class_key)
                    )


def parse_item_module(
    domain_item_module: ModuleType,
    root_module_name: str,
    domain_classes_by_fqdn: Dict[str, UmlClass],
    domain_compositions: List[UmlComposition]
):
    # processes only the classes imported and defined within the given root module
    for definition_type in filter_domain_definitions(domain_item_module, root_module_name):
        # definition_type_fqdn = definition_type.__module__
        definition_type_fqdn = f'{definition_type.__module__}.{definition_type.__name__}'
        if definition_type_fqdn not in domain_classes_by_fqdn:
            definition_attrs = []
            uml_class = UmlClass(
                name=definition_type.__name__,
                fqdn=definition_type_fqdn,
                attributes=definition_attrs
            )
            domain_classes_by_fqdn[definition_type_fqdn] = uml_class
            # inspect_type(definition_type)
            type_annotations = getattr(definition_type, '__annotations__', None)
            if type_annotations is not None:
                for attr_name, attr_class in type_annotations.items():
                    attr_raw_type = str(attr_class)
                    concrete_type_match = CONCRETE_TYPE_PATTERN.search(attr_raw_type)
                    if concrete_type_match:
                        concrete_type_fqdn = concrete_type_match.group(1)
                        if concrete_type_fqdn.startswith(root_module_name):
                            attr_type = attr_class.__name__
                            domain_compositions.append(
                                UmlComposition(uml_class.fqdn, f'{attr_class.__module__}.{attr_class.__name__}')
                            )
                        else:
                            attr_type = concrete_type_fqdn
                    else:
                        composition_rel = getattr(attr_class, '_name', None)
                        component_classes = getattr(attr_class, '__args__', None)
                        if composition_rel and component_classes:
                            component_names = [
                                component_class.__name__ if component_class.__module__.startswith(root_module_name) else f'{component_class.__module__}.{component_class.__name__}'
                                for component_class in component_classes
                            ]
                            domain_compositions.extend([
                                UmlComposition(uml_class.fqdn, f'{component_class.__module__}.{component_class.__name__}')
                                for component_class in component_classes
                                if component_class.__module__.startswith(root_module_name)
                            ])
                            attr_type = f"{composition_rel}[{', '.join(component_names)}]"
                        else:
                            attr_type = attr_raw_type
                    uml_attr = UmlAttribute(attr_name, attr_type)
                    definition_attrs.append(uml_attr)
