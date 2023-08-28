from typing import Dict, List

from py2puml.domain.umlclass import UmlClass
from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlrelation import UmlRelation
from py2puml.inspection.inspectmodule import inspect_domain_definition

from tests.asserts.attribute import assert_attribute
from tests.modules.withnamedtuple import Circle


def test_parse_namedtupled_class():
    domain_items_by_fqn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    inspect_domain_definition(Circle, 'tests.modules.withnamedtuple', domain_items_by_fqn, domain_relations)

    umlitems_by_fqn = list(domain_items_by_fqn.items())
    assert len(umlitems_by_fqn) == 1, 'one namedtuple must be inspected'
    namedtupled_class: UmlClass
    fqn, namedtupled_class = umlitems_by_fqn[0]
    assert fqn == 'tests.modules.withnamedtuple.Circle'
    assert namedtupled_class.fqn == fqn
    assert namedtupled_class.name == 'Circle'
    attributes = namedtupled_class.attributes
    assert len(attributes) == 3, '3 attributes must be detected in the namedtupled class'
    assert_attribute(attributes[0], 'x', 'Any', False)
    assert_attribute(attributes[1], 'y', 'Any', False)
    assert_attribute(attributes[2], 'radius', 'Any', False)

    assert len(domain_relations) == 0, 'inspecting namedtuple must add no relation'
