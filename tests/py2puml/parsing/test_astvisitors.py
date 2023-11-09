from ast import AST, get_source_segment, parse
from inspect import getsource
from textwrap import dedent
from typing import Dict, List, Tuple, Union

from pytest import mark

from py2puml.parsing.astvisitors import (
    AssignedVariablesCollector,
    SignatureVariablesCollector,
    shorten_compound_type_annotation,
)
from py2puml.parsing.moduleresolver import ModuleResolver

from tests.asserts.variable import assert_Variable
from tests.py2puml.parsing.mockedinstance import MockedInstance


class ParseMyConstructorArguments:
    def __init__(
        # the reference to the instance is often 'self' by convention, but can be anything else
        me,
        # some arguments, typed or untyped
        an_int: int,
        an_untyped,
        a_compound_type: Tuple[float, Dict[str, List[bool]]],
        # union types
        x_a: Union[int, float],
        y_a: Union[int, float, None],
        x_b: int | float,
        y_b: int | float | None,
        # an argument with a default value
        a_default_string: str = 'text',
        # positional and keyword wildcard arguments
        *args,
        **kwargs,
    ):
        pass


def test_SignatureVariablesCollector_collect_arguments():
    constructor_source: str = dedent(getsource(ParseMyConstructorArguments.__init__.__code__))
    constructor_ast: AST = parse(constructor_source)

    collector = SignatureVariablesCollector(constructor_source)
    collector.visit(constructor_ast)

    assert collector.class_self_id == 'me'
    assert len(collector.variables) == 10, 'all the arguments must be detected'
    assert_Variable(collector.variables[0], 'an_int', 'int', constructor_source)
    assert_Variable(collector.variables[1], 'an_untyped', None, constructor_source)
    assert_Variable(
        collector.variables[2], 'a_compound_type', 'Tuple[float, Dict[str, List[bool]]]', constructor_source
    )

    assert_Variable(collector.variables[3], 'x_a', 'Union[int, float]', constructor_source)
    assert_Variable(collector.variables[4], 'y_a', 'Union[int, float, None]', constructor_source)
    assert_Variable(collector.variables[5], 'x_b', 'int | float', constructor_source)
    assert_Variable(collector.variables[6], 'y_b', 'int | float | None', constructor_source)

    assert_Variable(collector.variables[7], 'a_default_string', 'str', constructor_source)
    assert_Variable(collector.variables[8], 'args', None, constructor_source)
    assert_Variable(collector.variables[9], 'kwargs', None, constructor_source)


@mark.parametrize(
    ['class_self_id', 'assignment_code', 'annotation_as_str', 'self_attributes', 'variables'],
    [
        # detects the assignment to a new variable
        ('self', 'my_var = 5', None, [], [('my_var', None)]),
        ('self', 'my_var: int = 5', 'int', [], [('my_var', 'int')]),
        # detects the assignment to a new self attribute
        ('self', 'self.my_attr = 6', None, [('my_attr', None)], []),
        ('self', 'self.my_attr: int = 6', 'int', [('my_attr', 'int')], []),
        # tuple assignment mixing variable and attribute
        ('self', 'my_var, self.my_attr = 5, 6', None, [('my_attr', None)], [('my_var', None)]),
        # assignment to a subscript of an attribute
        ('self', 'self.my_attr[0] = 0', None, [], []),
        ('self', 'self.my_attr[0]:int = 0', 'int', [], []),
        # assignment to an attribute of an attribute
        ('self', 'self.my_attr.id = "42"', None, [], []),
        ('self', 'self.my_attr.id: str = "42"', 'str', [], []),
        # assignment to an attribute of a reference which is not 'self'
        ('me', 'self.my_attr = 6', None, [], []),
        ('me', 'self.my_attr: int = 6', 'int', [], []),
    ],
)
def test_AssignedVariablesCollector_single_assignment_separate_variable_from_instance_attribute(
    class_self_id: str, assignment_code: str, annotation_as_str: str, self_attributes: list, variables: list
):
    # the assignment is the first line of the body
    assignment_ast: AST = parse(assignment_code).body[0]

    # assignment without annotation (multiple targets, but only one in these test cases)
    if annotation_as_str is None:
        annotation = None
        assert len(assignment_ast.targets) == 1, 'unit test consistency'
        assignment_target = assignment_ast.targets[0]
    # assignment with annotation (only one target)
    else:
        annotation = assignment_ast.annotation
        assert get_source_segment(assignment_code, annotation) == annotation_as_str, 'unit test consistency'
        assignment_target = assignment_ast.target

    assignment_collector = AssignedVariablesCollector(class_self_id, annotation)
    assignment_collector.visit(assignment_target)

    # detection of self attributes
    assert len(assignment_collector.self_attributes) == len(self_attributes)
    for self_attribute, (variable_id, variable_type_str) in zip(assignment_collector.self_attributes, self_attributes):
        assert_Variable(self_attribute, variable_id, variable_type_str, assignment_code)

    # detection of new variables occupying the memory scope
    assert len(assignment_collector.variables) == len(variables)
    for variable, (variable_id, variable_type_str) in zip(assignment_collector.variables, variables):
        assert_Variable(variable, variable_id, variable_type_str, assignment_code)


@mark.parametrize(
    ['class_self_id', 'assignment_code', 'self_attributes_and_variables_by_target'],
    [
        (
            'self',
            'x = y = 0',
            [
                ([], ['x']),
                ([], ['y']),
            ],
        ),
        (
            'self',
            'self.x = self.y = 0',
            [
                (['x'], []),
                (['y'], []),
            ],
        ),
        (
            'self',
            'self.my_attr = self.my_list[0] = 5',
            [
                (['my_attr'], []),
                ([], []),
            ],
        ),
        (
            'self',
            'self.x, self.y = self.origin = (0, 0)',
            [
                (['x', 'y'], []),
                (['origin'], []),
            ],
        ),
    ],
)
def test_AssignedVariablesCollector_multiple_assignments_separate_variable_from_instance_attribute(
    class_self_id: str, assignment_code: str, self_attributes_and_variables_by_target: tuple
):
    # the assignment is the first line of the body
    assignment_ast: AST = parse(assignment_code).body[0]

    assert len(assignment_ast.targets) == len(
        self_attributes_and_variables_by_target
    ), 'test consistency: all targets must be tested'
    for assignment_target, (self_attribute_ids, variable_ids) in zip(
        assignment_ast.targets, self_attributes_and_variables_by_target
    ):
        assignment_collector = AssignedVariablesCollector(class_self_id, None)
        assignment_collector.visit(assignment_target)

        assert len(assignment_collector.self_attributes) == len(self_attribute_ids), 'test consistency'
        for self_attribute, self_attribute_id in zip(assignment_collector.self_attributes, self_attribute_ids):
            assert self_attribute.id == self_attribute_id
            assert self_attribute.type_expr is None, 'Python does not allow type annotation in multiple assignment'

        assert len(assignment_collector.variables) == len(variable_ids), 'test consistency'
        for variable, variable_id in zip(assignment_collector.variables, variable_ids):
            assert variable.id == variable_id
            assert variable.type_expr is None, 'Python does not allow type annotation in multiple assignment'


@mark.parametrize(
    ['full_annotation', 'short_annotation', 'namespaced_definitions', 'module_dict'],
    [
        (
            # domain.people was imported, people.Person is used
            'people.Person',
            'Person',
            ['domain.people.Person'],
            {'__name__': 'testmodule', 'people': {'Person': {'__module__': 'domain.people', '__name__': 'Person'}}},
        ),
        (
            # combination of compound types
            'Dict[id.Identifier,typing.List[domain.Person]]',
            'Dict[Identifier, List[Person]]',
            ['typing.Dict', 'id.Identifier', 'typing.List', 'domain.Person'],
            {
                '__name__': 'testmodule',
                'Dict': Dict,
                'List': List,
                'id': {
                    'Identifier': {
                        '__module__': 'id',
                        '__name__': 'Identifier',
                    }
                },
                'domain': {
                    'Person': {
                        '__module__': 'domain',
                        '__name__': 'Person',
                    }
                },
            },
        ),
        (
            # union types
            'Dict[typing.Union[int,id.Identifier],str|domain.Person]',
            'Dict[Union[int, Identifier], str | Person]',
            ['typing.Dict', 'typing.Union', 'builtins.int', 'id.Identifier', 'builtins.str', 'domain.Person'],
            {
                '__name__': 'testmodule',
                '__builtins__': {
                    'int': {
                        '__module__': 'builtins',
                        '__name__': 'int',
                    },
                    'str': {
                        '__module__': 'builtins',
                        '__name__': 'str',
                    },
                },
                'Dict': Dict,
                'List': List,
                'Union': Union,
                'id': {
                    'Identifier': {
                        '__module__': 'id',
                        '__name__': 'Identifier',
                    }
                },
                'domain': {
                    'Person': {
                        '__module__': 'domain',
                        '__name__': 'Person',
                    }
                },
            },
        ),
    ],
)
def test_shorten_compound_type_annotation(
    full_annotation: str, short_annotation: str, namespaced_definitions: List[str], module_dict: dict
):
    module_resolver = ModuleResolver(MockedInstance(module_dict))
    shortened_annotation, full_namespaced_definitions = shorten_compound_type_annotation(
        full_annotation, module_resolver
    )
    assert shortened_annotation == short_annotation
    assert full_namespaced_definitions == namespaced_definitions
