
from importlib import import_module

from py2puml.domain.umlclass import UmlClass, UmlAttribute
from py2puml.domain.umlrelation import UmlRelation, RelType
from py2puml.inspection.inspectmodule import inspect_module
from py2puml.parsing.astvisitors import ConstructorVisitor
from py2puml.parsing.moduleresolver import ModuleResolver
from py2puml.parsing.parseclassconstructor import parse_class_constructor

from tests.asserts.attribute import assert_attribute
from tests.asserts.relation import assert_relation


def test_inspect_module_should_find_static_and_instance_attributes():
    domain_items_by_fqn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    inspect_module(
        import_module('tests.modules.withconstructor'),
        'tests.modules.withconstructor',
        domain_items_by_fqn, domain_relations
    )

    assert len(domain_items_by_fqn) == 2, 'two classes must be inspected'

    # Coordinates UmlClass
    coordinates_umlitem: UmlClass = domain_items_by_fqn['tests.modules.withconstructor.Coordinates']
    assert len(coordinates_umlitem.attributes) == 2, '2 attributes of Coordinates must be inspected'
    x_attribute, y_attribute = coordinates_umlitem.attributes
    assert_attribute(x_attribute, 'x', 'float', expected_staticity=False)
    assert_attribute(y_attribute, 'y', 'float', expected_staticity=False)

    # Point UmlClass
    point_umlitem: UmlClass = domain_items_by_fqn['tests.modules.withconstructor.Point']
    point_expected_attributes = {
        'PI': ('float', True),
        # 'origin': (None, True), # not annotated class variable -> not handled for now
        'coordinates': ('Coordinates', False),
        'day_unit': ('TimeUnit', False),
        'hour_unit': ('TimeUnit', False),
        'time_resolution': ('Tuple[str, TimeUnit]', False),
        'x': ('int', False),
        'y': ('str', False),
        'x_unit': ('str', False),
        'y_unit': ('str', False),
        'z': (None, False),
        'w': ('int', False),
        'u': (None, False),
        'v': (None, False),
        'dates': ('List[date]', False),
    }
    assert len(point_umlitem.attributes) == len(point_expected_attributes), 'all Point attributes must be verified'
    for attribute_name, (atrribute_type, attribute_staticity) in point_expected_attributes.items():
        point_attribute: UmlAttribute = next((
            attribute
            for attribute in point_umlitem.attributes
            if attribute.name == attribute_name
        ), None)
        assert point_attribute is not None, f'attribute {attribute_name} must be detected'
        assert_attribute(point_attribute, attribute_name, atrribute_type, expected_staticity=attribute_staticity)

    # Coordinates is a component of Point
    assert len(domain_relations) == 1, '1 composition'
    assert_relation(
        domain_relations[0],
        'tests.modules.withconstructor.Point',
        'tests.modules.withconstructor.Coordinates',
        RelType.COMPOSITION
    )

def test_inspect_module_parse_class_constructor_should_not_process_inherited_constructor():
    domain_items_by_fqn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    # inspects the two sub-modules
    inspect_module(
        import_module('tests.modules.withinheritedconstructor.point'),
        'tests.modules.withinheritedconstructor.point',
        domain_items_by_fqn, domain_relations
    )
    inspect_module(
        import_module('tests.modules.withinheritedconstructor.metricorigin'),
        'tests.modules.withinheritedconstructor.metricorigin',
        domain_items_by_fqn, domain_relations
    )

    assert len(domain_items_by_fqn) == 3, 'three classes must be inspected'

    # Point UmlClass
    point_umlitem: UmlClass = domain_items_by_fqn['tests.modules.withinheritedconstructor.point.Point']
    assert len(point_umlitem.attributes) == 2, '2 attributes of Point must be inspected'
    x_attribute, y_attribute = point_umlitem.attributes
    assert_attribute(x_attribute, 'x', 'float', expected_staticity=False)
    assert_attribute(y_attribute, 'y', 'float', expected_staticity=False)

    # Origin UmlClass
    origin_umlitem: UmlClass = domain_items_by_fqn['tests.modules.withinheritedconstructor.point.Origin']
    assert len(origin_umlitem.attributes) == 1, '1 attribute of Origin must be inspected'
    is_origin_attribute = origin_umlitem.attributes[0]
    assert_attribute(is_origin_attribute, 'is_origin', 'bool', expected_staticity=True)

    # MetricOrigin UmlClass
    metric_origin_umlitem: UmlClass = domain_items_by_fqn['tests.modules.withinheritedconstructor.metricorigin.MetricOrigin']
    assert len(metric_origin_umlitem.attributes) == 1, '1 attribute of MetricOrigin must be inspected'
    unit_attribute = metric_origin_umlitem.attributes[0]
    assert_attribute(unit_attribute, 'unit', 'str', expected_staticity=True)
