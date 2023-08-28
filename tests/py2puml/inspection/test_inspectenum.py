from typing import Dict, List

from py2puml.domain.umlenum import Member, UmlEnum
from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlrelation import UmlRelation
from py2puml.inspection.inspectmodule import inspect_domain_definition

from tests.modules.withenum import TimeUnit


def assert_member(member: Member, expected_name: str, expected_value: str):
    assert member.name == expected_name
    assert member.value == expected_value


def test_inspect_enum_type():
    domain_items_by_fqn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    inspect_domain_definition(TimeUnit, 'tests.modules.withenum', domain_items_by_fqn, domain_relations)

    umlitems_by_fqn = list(domain_items_by_fqn.items())
    assert len(umlitems_by_fqn) == 1, 'one enum must be inspected'
    umlenum: UmlEnum
    fqn, umlenum = umlitems_by_fqn[0]
    assert fqn == 'tests.modules.withenum.TimeUnit'
    assert umlenum.fqn == fqn
    assert umlenum.name == 'TimeUnit'
    members: List[Member] = umlenum.members
    assert len(members) == 3, 'enum has 3 members'
    assert_member(members[0], 'DAYS', 'd')
    assert_member(members[1], 'HOURS', 'h')
    assert_member(members[2], 'MINUTE', 'm')

    assert len(domain_relations) == 0, 'inspecting enum must add no relation'
