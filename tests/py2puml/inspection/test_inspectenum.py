
from typing import Dict, List

from py2puml.domain.umlenum import UmlEnum, Member
from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlrelation import UmlRelation
from py2puml.inspection.inspectmodule import inspect_type

from tests.modules.withenum import TimeUnit

def assert_member(member: Member, expected_name: str, expected_value: str):
    assert member.name == expected_name
    assert member.value == expected_value

def test_inspect_enum_type():
    domain_items_by_fqdn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    inspect_type(TimeUnit, 'tests.modules.withenum', domain_items_by_fqdn, domain_relations)

    umlitems_by_fqdn = list(domain_items_by_fqdn.items())
    assert len(umlitems_by_fqdn) == 1, 'one enum has been parsed'
    umlenum: UmlEnum
    fqdn, umlenum = umlitems_by_fqdn[0]
    assert fqdn == 'tests.modules.withenum.TimeUnit'
    assert umlenum.fqdn == fqdn
    assert umlenum.name == 'TimeUnit'
    members: List[Member] = umlenum.members
    assert len(members) == 3, 'enum has 3 members'
    assert_member(members[0], 'DAYS', 'd')
    assert_member(members[1], 'HOURS', 'h')
    assert_member(members[2], 'MINUTE', 'm')

    assert len(domain_relations) == 0, 'parsing enum adds no relation'
