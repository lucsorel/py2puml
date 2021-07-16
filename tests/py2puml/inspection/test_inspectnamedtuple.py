
from typing import Dict, List
from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlclass import UmlClass
from py2puml.domain.umlrelation import UmlRelation
from py2puml.inspection.inspectmodule import inspect_type

from tests.modules.withnamedtuple import Circle
from tests.py2puml.inspection.test_inspectclass import assert_attribute

def test_parse_namedtupled_class():
    domain_items_by_fqdn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    inspect_type(Circle, 'tests.modules.withnamedtuple', domain_items_by_fqdn, domain_relations)

    umlitems_by_fqdn = list(domain_items_by_fqdn.items())
    assert len(umlitems_by_fqdn) == 1, 'one namedtupled class has been parsed'
    namedtupled_class: UmlClass
    fqdn, namedtupled_class = umlitems_by_fqdn[0]
    assert fqdn == 'tests.modules.withnamedtuple.Circle'
    assert namedtupled_class.fqdn == fqdn
    assert namedtupled_class.name == 'Circle'
    attributes = namedtupled_class.attributes
    assert len(attributes) == 3, 'namedtupled class has 3 attributes'
    assert_attribute(attributes[0], 'x', 'Any')
    assert_attribute(attributes[1], 'y', 'Any')
    assert_attribute(attributes[2], 'radius', 'Any')

    assert len(domain_relations) == 0, 'parsing enum adds no relation'
