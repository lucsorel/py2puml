from importlib import import_module
from typing import Callable, Dict

from pytest import fixture

from py2puml.domain.umlitem import UmlItem
from py2puml.inspection.inspectmodule import inspect_module

from tests.asserts.attribute import assert_attribute


@fixture(scope='module', autouse=True)
def inspected_union_types_items() -> Dict[str, UmlItem]:
    """
    Inspects the test module containing several types involving union types, once for all the unit tests involved in this module
    """
    fqdn = 'tests.modules.withuniontypes'
    domain_items_by_fqn: Dict[str, UmlItem] = {}
    inspect_module(import_module(fqdn), fqdn, domain_items_by_fqn, [])

    assert len(domain_items_by_fqn) == 5, 'five union-typed classes must be inspected'

    return domain_items_by_fqn


@fixture(scope='function')
def get_union_type_item(inspected_union_types_items: Dict[str, UmlItem]) -> Callable[[str], UmlItem]:
    return lambda class_name: inspected_union_types_items[f'tests.modules.withuniontypes.{class_name}']


def test_union_type_number_wrapper(get_union_type_item: Callable[[str], UmlItem]):
    umlitem = get_union_type_item('NumberWrapper')

    assert len(umlitem.attributes) == 1, '1 attribute of NumberWrapper must be inspected'
    number_attribute = umlitem.attributes[0]
    assert_attribute(number_attribute, 'number', 'Union[int, float]', expected_staticity=False)


def test_union_type_optional_number_wrapper(get_union_type_item: Callable[[str], UmlItem]):
    umlitem = get_union_type_item('OptionalNumberWrapper')

    assert len(umlitem.attributes) == 1, '1 attribute of OptionalNumberWrapper must be inspected'
    number_attribute = umlitem.attributes[0]
    assert_attribute(number_attribute, 'number', 'Union[int, float, None]', expected_staticity=False)


def test_union_type_number_wrapper_py3_10(get_union_type_item: Callable[[str], UmlItem]):
    umlitem = get_union_type_item('NumberWrapperPy3_10')

    assert len(umlitem.attributes) == 1, '1 attribute of NumberWrapperPy3_10 must be inspected'
    number_attribute = umlitem.attributes[0]
    assert_attribute(number_attribute, 'number', 'int | float', expected_staticity=False)


def test_union_type_optional_number_wrapper_py3_10(get_union_type_item: Callable[[str], UmlItem]):
    umlitem = get_union_type_item('OptionalNumberWrapperPy3_10')

    assert len(umlitem.attributes) == 1, '1 attribute of OptionalNumberWrapperPy3_10 must be inspected'
    number_attribute = umlitem.attributes[0]
    assert_attribute(number_attribute, 'number', 'int | float | None', expected_staticity=False)


def test_union_type_distance_calculator(get_union_type_item: Callable[[str], UmlItem]):
    umlitem = get_union_type_item('DistanceCalculator')

    assert len(umlitem.attributes) == 5, '5 attributes of DistanceCalculator must be inspected'

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
