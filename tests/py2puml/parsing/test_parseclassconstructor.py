
from py2puml.inspection.inspectmodule import inspect_module
from py2puml.parsing.astvisitors import ConstructorVisitor
from py2puml.parsing.moduleresolver import ModuleResolver
from py2puml.parsing.parseclassconstructor import parse_class_constructor

from tests.modules.withconstructor import Point


def test_parse_class_constructor():
    uml_attributes, uml_relations_by_fqdn = parse_class_constructor(
        Point,
        'tests.modules.withconstructor.Point',
        'tests'
    )
    print('uml_attributes', uml_attributes)
    assert len(uml_attributes) == 11

