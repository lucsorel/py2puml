from typing import Dict, List

from py2puml.parser import parse_type, parse_enum_type
from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlclass import UmlClass, UmlAttribute
from py2puml.domain.umlenum import UmlEnum, Member
from py2puml.domain.umlrelation import UmlRelation

from tests.modules.withbasictypes import Contact
from tests.modules.withcomposition import Worker
from tests.modules.withenum import TimeUnit

def assert_attribute(attribute: UmlAttribute, expected_name: str, expected_type: str):
    assert attribute.name == expected_name
    assert attribute.type == expected_type

def assert_member(member: Member, expected_name: str, expected_value: str):
    assert member.name == expected_name
    assert member.value == expected_value


def test_parse_type_single_class_without_composition():
    domain_items_by_fqdn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    parse_type(Contact, 'tests.modules.withbasictypes', domain_items_by_fqdn, domain_relations)

    umlitems_by_fqdn = list(domain_items_by_fqdn.items())
    assert len(umlitems_by_fqdn) == 1, 'one class has been parsed'

    umlclass: UmlClass
    fqdn, umlclass = umlitems_by_fqdn[0]
    assert fqdn == 'tests.modules.withbasictypes.Contact'
    assert umlclass.fqdn == fqdn
    assert umlclass.name == 'Contact'
    attributes = umlclass.attributes
    assert len(attributes) == 4, 'class has 4 attributes'
    assert_attribute(attributes[0], 'full_name', 'str')
    assert_attribute(attributes[1], 'age', 'int')
    assert_attribute(attributes[2], 'weight', 'float')
    assert_attribute(attributes[3], 'can_twist_tongue', 'bool')

    assert len(domain_relations) == 0, 'class has no component'

def test_parse_type_single_class_with_composition():
    domain_items_by_fqdn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    parse_type(Worker, 'tests.modules.withcomposition', domain_items_by_fqdn, domain_relations)

    umlitems_by_fqdn = list(domain_items_by_fqdn.items())
    assert len(umlitems_by_fqdn) == 1, 'one class has been parsed'

    assert len(domain_relations) == 1, 'class has 1 domain component'
    assert domain_relations[0].source_fqdn == 'tests.modules.withcomposition.Worker'
    assert domain_relations[0].target_fqdn == 'tests.modules.withcomposition.Address'

def test_parse_enum_type():
    domain_items_by_fqdn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    parse_type(TimeUnit, 'tests.modules.withenum', domain_items_by_fqdn, domain_relations)

    umlitems_by_fqdn = list(domain_items_by_fqdn.items())
    assert len(umlitems_by_fqdn) == 1, 'one enum has been parsed'
    umlenum: UmlEnum
    fqdn, umlenum = umlitems_by_fqdn[0]
    assert fqdn == 'tests.modules.withenum.TimeUnit'
    assert umlenum.fqdn == fqdn
    assert umlenum.name == 'TimeUnit'
    members = umlenum.members
    assert len(members) == 3, 'enum has 3 members'
    assert_member(members[0], 'DAYS', 'd')
    assert_member(members[1], 'HOURS', 'h')
    assert_member(members[2], 'MINUTE', 'm')

    assert len(domain_relations) == 0, 'parsing enum adds no relation'
