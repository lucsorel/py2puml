from importlib import import_module
from typing import Dict, List

from py2puml.domain.umlclass import UmlClass
from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlrelation import UmlRelation
from py2puml.inspection.inspectmodule import inspect_module

from tests.asserts.attribute import assert_attribute


def test_inspect_dataclasses_and_class_with_union_types(
    domain_items_by_fqn: Dict[str, UmlItem], domain_relations: List[UmlRelation]
):
    fqdn = 'tests.modules.withuniontypes'
    inspect_module(import_module(fqdn), fqdn, domain_items_by_fqn, domain_relations)

    assert len(domain_items_by_fqn) == 5, 'five classes must be inspected'

    # NumberWrapper UmlClass
    umlitem: UmlClass = domain_items_by_fqn[f'{fqdn}.NumberWrapper']
    assert len(umlitem.attributes) == 1, '1 attribute of NumberWrapper must be inspected'
    number_attribute = umlitem.attributes[0]
    assert_attribute(number_attribute, 'number', 'Union[int, float]', expected_staticity=False)

    # OptionalNumberWrapper UmlClass
    umlitem: UmlClass = domain_items_by_fqn[f'{fqdn}.OptionalNumberWrapper']
    assert len(umlitem.attributes) == 1, '1 attribute of OptionalNumberWrapper must be inspected'
    number_attribute = umlitem.attributes[0]
    assert_attribute(number_attribute, 'number', 'Union[int, float, None]', expected_staticity=False)

    # NumberWrapperPy3_10 UmlClass
    umlitem: UmlClass = domain_items_by_fqn[f'{fqdn}.NumberWrapperPy3_10']
    assert len(umlitem.attributes) == 1, '1 attribute of NumberWrapperPy3_10 must be inspected'
    number_attribute = umlitem.attributes[0]
    assert_attribute(number_attribute, 'number', 'int | float', expected_staticity=False)

    # OptionalNumberWrapperPy3_10 UmlClass
    umlitem: UmlClass = domain_items_by_fqn[f'{fqdn}.OptionalNumberWrapperPy3_10']
    assert len(umlitem.attributes) == 1, '1 attribute of OptionalNumberWrapperPy3_10 must be inspected'
    number_attribute = umlitem.attributes[0]
    assert_attribute(number_attribute, 'number', 'int | float | None', expected_staticity=False)

    # DistanceCalculator UmlClass
    umlitem: UmlClass = domain_items_by_fqn[f'{fqdn}.DistanceCalculator']
    assert len(umlitem.attributes) == 5, '5 attributes of DistanceCalculator must be inspected'
    print(f'{umlitem.attributes=}')
    x_a_attribute = umlitem.attributes[0]
    assert_attribute(x_a_attribute, 'x_a', 'Union[int, float]', expected_staticity=False)
    y_a_attribute = umlitem.attributes[1]
    assert_attribute(y_a_attribute, 'y_a', 'Union[int, float, None]', expected_staticity=False)
    x_b_attribute = umlitem.attributes[2]
    assert_attribute(x_b_attribute, 'x_b', 'int | float', expected_staticity=False)
    y_b_attribute = umlitem.attributes[3]
    assert_attribute(y_b_attribute, 'y_b', 'int | float | None', expected_staticity=False)
    space_characs_attribute = umlitem.attributes[4]
    assert_attribute(space_characs_attribute, 'space_characs', 'str | None', expected_staticity=False)
