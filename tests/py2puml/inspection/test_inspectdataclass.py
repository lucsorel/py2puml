from typing import Dict, List

from py2puml.domain.umlclass import UmlClass
from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlrelation import RelType, UmlRelation
from py2puml.inspection.inspectmodule import inspect_domain_definition

from tests.asserts.attribute import assert_attribute
from tests.asserts.relation import assert_relation
from tests.modules.withbasictypes import Contact
from tests.modules.withcomposition import Worker
from tests.modules.withinheritancewithinmodule import GlowingFish


def test_inspect_domain_definition_single_class_without_composition():
    domain_items_by_fqn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    inspect_domain_definition(Contact, 'tests.modules.withbasictypes', domain_items_by_fqn, domain_relations)

    umlitems_by_fqn = list(domain_items_by_fqn.items())
    assert len(umlitems_by_fqn) == 1, 'one class must be inspected'

    umlclass: UmlClass
    fqn, umlclass = umlitems_by_fqn[0]
    assert fqn == 'tests.modules.withbasictypes.Contact'
    assert umlclass.fqn == fqn
    assert umlclass.name == 'Contact'
    attributes = umlclass.attributes
    assert len(attributes) == 4, 'class has 4 attributes'
    assert_attribute(attributes[0], 'full_name', 'str', expected_staticity=False)
    assert_attribute(attributes[1], 'age', 'int', expected_staticity=False)
    assert_attribute(attributes[2], 'weight', 'float', expected_staticity=False)
    assert_attribute(attributes[3], 'can_twist_tongue', 'bool', expected_staticity=False)

    assert len(domain_relations) == 0, 'no component must be detected in this class'


def test_inspect_domain_definition_single_class_with_composition():
    domain_items_by_fqn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    inspect_domain_definition(Worker, 'tests.modules.withcomposition', domain_items_by_fqn, domain_relations)

    assert len(domain_items_by_fqn) == 1, 'one class must be inspected'
    assert len(domain_relations) == 2, 'class has 2 domain components'
    # forward reference to colleagues
    assert_relation(
        domain_relations[0],
        'tests.modules.withcomposition.Worker',
        'tests.modules.withcomposition.Worker',
        RelType.COMPOSITION,
    )
    # adress of worker
    assert_relation(
        domain_relations[1],
        'tests.modules.withcomposition.Worker',
        'tests.modules.withcomposition.Address',
        RelType.COMPOSITION,
    )


def test_parse_inheritance_within_module():
    domain_items_by_fqn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    inspect_domain_definition(
        GlowingFish, 'tests.modules.withinheritancewithinmodule', domain_items_by_fqn, domain_relations
    )

    umlitems_by_fqn = list(domain_items_by_fqn.values())
    assert len(umlitems_by_fqn) == 1, 'the class with multiple inheritance was inspected'
    child_glowing_fish: UmlClass = umlitems_by_fqn[0]
    assert child_glowing_fish.name == 'GlowingFish'
    assert child_glowing_fish.fqn == 'tests.modules.withinheritancewithinmodule.GlowingFish'
    assert len(child_glowing_fish.attributes) == 2
    assert_attribute(child_glowing_fish.attributes[0], 'glow_for_hunting', 'bool', expected_staticity=False)
    assert_attribute(child_glowing_fish.attributes[1], 'glow_for_mating', 'bool', expected_staticity=False)

    assert len(domain_relations) == 2, '2 inheritance relations must be inspected'
    parent_fish, parent_light = domain_relations

    assert_relation(
        parent_fish,
        'tests.modules.withinheritancewithinmodule.Fish',
        'tests.modules.withinheritancewithinmodule.GlowingFish',
        RelType.INHERITANCE,
    )
    assert_relation(
        parent_light,
        'tests.modules.withinheritancewithinmodule.Light',
        'tests.modules.withinheritancewithinmodule.GlowingFish',
        RelType.INHERITANCE,
    )
