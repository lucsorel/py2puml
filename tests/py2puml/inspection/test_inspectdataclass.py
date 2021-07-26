
from typing import Dict, List, Tuple

from py2puml.inspection.inspectmodule import inspect_domain_definition
from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlclass import UmlClass, UmlAttribute
from py2puml.domain.umlrelation import UmlRelation, RelType

from tests.asserts.attribute import assert_attribute
from tests.asserts.relation import assert_relation
from tests.modules.withbasictypes import Contact
from tests.modules.withcomposition import Worker
from tests.modules.withinheritancewithinmodule import GlowingFish


def test_inspect_domain_definition_single_class_without_composition():
    domain_items_by_fqdn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    inspect_domain_definition(Contact, 'tests.modules.withbasictypes', domain_items_by_fqdn, domain_relations)

    umlitems_by_fqdn = list(domain_items_by_fqdn.items())
    assert len(umlitems_by_fqdn) == 1, 'one class must be inspected'

    umlclass: UmlClass
    fqdn, umlclass = umlitems_by_fqdn[0]
    assert fqdn == 'tests.modules.withbasictypes.Contact'
    assert umlclass.fqdn == fqdn
    assert umlclass.name == 'Contact'
    attributes = umlclass.attributes
    assert len(attributes) == 4, 'class has 4 attributes'
    assert_attribute(attributes[0], 'full_name', 'str', False)
    assert_attribute(attributes[1], 'age', 'int', False)
    assert_attribute(attributes[2], 'weight', 'float', False)
    assert_attribute(attributes[3], 'can_twist_tongue', 'bool', False)

    assert len(domain_relations) == 0, 'no component must be detected in this class'

def test_inspect_domain_definition_single_class_with_composition():
    domain_items_by_fqdn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    inspect_domain_definition(Worker, 'tests.modules.withcomposition', domain_items_by_fqdn, domain_relations)

    assert len(domain_items_by_fqdn) == 1, 'one class must be inspected'

    assert len(domain_relations) == 1, 'class has 1 domain component'
    assert_relation(
        domain_relations[0],
        'tests.modules.withcomposition.Worker',
        'tests.modules.withcomposition.Address',
        RelType.COMPOSITION
    )


def test_parse_inheritance_within_module():
    domain_items_by_fqdn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    inspect_domain_definition(GlowingFish, 'tests.modules.withinheritancewithinmodule', domain_items_by_fqdn, domain_relations)

    umlitems_by_fqdn = list(domain_items_by_fqdn.values())
    assert len(umlitems_by_fqdn) == 1, 'the class with multiple inheritance was inspected'
    child_glowing_fish: UmlClass = umlitems_by_fqdn[0]
    assert child_glowing_fish.name == 'GlowingFish'
    assert child_glowing_fish.fqdn == 'tests.modules.withinheritancewithinmodule.GlowingFish'

    assert len(domain_relations) == 2, '2 inheritance relations must be inspected'
    parent_fish, parent_light = domain_relations

    assert_relation(
        parent_fish,
        'tests.modules.withinheritancewithinmodule.Fish',
        'tests.modules.withinheritancewithinmodule.GlowingFish',
        RelType.INHERITANCE
    )
    assert_relation(
        parent_light,
        'tests.modules.withinheritancewithinmodule.Light',
        'tests.modules.withinheritancewithinmodule.GlowingFish',
        RelType.INHERITANCE
    )
