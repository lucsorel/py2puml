
from ast import parse
from importlib import import_module
from inspect import getsource
from textwrap import dedent

from py2puml.parsing.astvisitors import ConstructorVisitor
from py2puml.parsing.moduleresolver import ModuleResolver

from tests.modules.withconstructor import Point


def test_parse_constructor():
    constructor_source = getsource(Point.__init__.__code__)
    tree = parse(dedent(constructor_source))

    class_module = import_module(Point.__module__)
    module_resolver = ModuleResolver(class_module)

    visitor = ConstructorVisitor(dedent(constructor_source), Point.__name__, 'tests.modules', module_resolver)
    visitor.visit(tree)
    print('visitor.class_self_id', visitor.class_self_id)
    print('visitor.variables_namespace', visitor.variables_namespace)
    print('visitor.uml_attributes', visitor.uml_attributes)
    print('visitor.uml_relations_by_target_fqdn', visitor.uml_relations_by_target_fqdn)
    # print(hasattr(class_module, 'Coordinates'))
    # print(class_module.Coordinates.__module__)
    # print(class_module.modules.withenum.TimeUnit.__module__)
    # print(class_module.withenum.TimeUnit.__module__)
    assert len(visitor.uml_attributes) == 12
