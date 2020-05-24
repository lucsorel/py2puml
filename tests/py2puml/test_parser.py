from typing import Dict, List

from py2puml.parser import parse_type
from py2puml.domain.umlclass import UmlClass, UmlAttribute
from py2puml.domain.umlcomposition import UmlComposition

from tests.modules.withbasictypes import Contact
from tests.modules.withcomposition import Worker

def assert_attribute(attribute: UmlAttribute, expected_name: str, expected_type: str):
    assert attribute.name == expected_name
    assert attribute.type == expected_type

def test_parse_type_single_class_without_composition():
    domain_classes_by_fqdn: Dict[str, UmlClass] = {}
    domain_compositions: List[UmlComposition] = []
    parse_type(Contact, 'tests.modules.withbasictypes', domain_classes_by_fqdn, domain_compositions)

    umlclasses_by_fqdn = list(domain_classes_by_fqdn.items())
    assert len(umlclasses_by_fqdn) == 1, 'one class has been parsed'

    umlclass: UmlClass
    fqdn, umlclass = umlclasses_by_fqdn[0]
    assert fqdn == 'tests.modules.withbasictypes.Contact'
    assert umlclass.fqdn == fqdn
    assert umlclass.name == 'Contact'
    attributes = umlclass.attributes
    assert len(attributes) == 4, 'class has 4 attributes'
    assert_attribute(attributes[0], 'full_name', 'str')
    assert_attribute(attributes[1], 'age', 'int')
    assert_attribute(attributes[2], 'weight', 'float')
    assert_attribute(attributes[3], 'can_twist_tongue', 'bool')

    assert len(domain_compositions) == 0, 'class has no component'

def test_parse_type_single_class_with_composition():
    domain_classes_by_fqdn: Dict[str, UmlClass] = {}
    domain_compositions: List[UmlComposition] = []
    parse_type(Worker, 'tests.modules.withcomposition', domain_classes_by_fqdn, domain_compositions)

    umlclasses_by_fqdn = list(domain_classes_by_fqdn.items())
    assert len(umlclasses_by_fqdn) == 1, 'one class has been parsed'

    assert len(domain_compositions) == 1, 'class has 1 domain component'
    assert domain_compositions[0].compound_fqdn == 'tests.modules.withcomposition.Worker'
    assert domain_compositions[0].component_fqdn == 'tests.modules.withcomposition.Address'