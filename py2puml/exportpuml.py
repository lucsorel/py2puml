from typing import List, Iterable

from py2puml.domain.umlclass import UmlClass
from py2puml.domain.umlcomposition import UmlComposition

PUML_FILE_START = '@startuml\n'
PUML_FILE_END = '@enduml\n'
PUML_CLASS_START_TPL = 'class {class_fqdn} {{\n'
PUML_ATTR_TPL = '  {attr_name}: {attr_type}\n'
PUML_CLASS_END = '}\n'
PUML_COMPOSITION_TPL = '{compound_fqdn} *-- {component_fqdn}\n'


def to_puml_content(uml_classes: List[UmlClass], uml_compositions: List[UmlComposition]) -> Iterable[str]:
    yield PUML_FILE_START
    for uml_class in uml_classes:
        yield PUML_CLASS_START_TPL.format(class_fqdn=uml_class.fqdn)
        for uml_attr in uml_class.attributes:
            yield PUML_ATTR_TPL.format(attr_type=uml_attr.type, attr_name=uml_attr.name)
        yield PUML_CLASS_END
    for uml_composition in uml_compositions:
        yield PUML_COMPOSITION_TPL.format(compound_fqdn=uml_composition.compound_fqdn, component_fqdn=uml_composition.component_fqdn)
    yield PUML_FILE_END
