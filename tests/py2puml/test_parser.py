from typing import Dict, List

from py2puml.parser import parse_type, parse_enum_type
from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlclass import UmlClass, UmlAttribute
from py2puml.domain.umlenum import UmlEnum, Member
from py2puml.domain.umlrelation import UmlRelation, RelType

from tests.modules.withbasictypes import Contact
from tests.modules.withcomposition import Worker
from tests.modules.withenum import TimeUnit
from tests.modules.withinheritancewithinmodule import GlowingFish
from tests.modules.withnamedtuple import Circle
from tests.modules.withconstructor import Point

def assert_attribute(attribute: UmlAttribute, expected_name: str, expected_type: str):
    assert attribute.name == expected_name
    assert attribute.type == expected_type

def assert_member(member: Member, expected_name: str, expected_value: str):
    assert member.name == expected_name
    assert member.value == expected_value


def test_parse_type_single_class_without_composition():
    domain_items_by_fqdn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    parse_type(Contact, 'tests.modules.withbasictypes', domain_items_by_fqdn, domain_relations)

    umlitems_by_fqdn = list(domain_items_by_fqdn.items())
    assert len(umlitems_by_fqdn) == 1, 'one class has been parsed'

    umlclass: UmlClass
    fqdn, umlclass = umlitems_by_fqdn[0]
    assert fqdn == 'tests.modules.withbasictypes.Contact'
    assert umlclass.fqdn == fqdn
    assert umlclass.name == 'Contact'
    attributes = umlclass.attributes
    assert len(attributes) == 4, 'class has 4 attributes'
    assert_attribute(attributes[0], 'full_name', 'str')
    assert_attribute(attributes[1], 'age', 'int')
    assert_attribute(attributes[2], 'weight', 'float')
    assert_attribute(attributes[3], 'can_twist_tongue', 'bool')

    assert len(domain_relations) == 0, 'class has no component'

def test_parse_type_single_class_with_composition():
    domain_items_by_fqdn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    parse_type(Worker, 'tests.modules.withcomposition', domain_items_by_fqdn, domain_relations)

    umlitems_by_fqdn = list(domain_items_by_fqdn.items())
    assert len(umlitems_by_fqdn) == 1, 'one class has been parsed'

    assert len(domain_relations) == 1, 'class has 1 domain component'
    assert domain_relations[0].source_fqdn == 'tests.modules.withcomposition.Worker'
    assert domain_relations[0].target_fqdn == 'tests.modules.withcomposition.Address'

def test_parse_enum_type():
    domain_items_by_fqdn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    parse_type(TimeUnit, 'tests.modules.withenum', domain_items_by_fqdn, domain_relations)

    umlitems_by_fqdn = list(domain_items_by_fqdn.items())
    assert len(umlitems_by_fqdn) == 1, 'one enum has been parsed'
    umlenum: UmlEnum
    fqdn, umlenum = umlitems_by_fqdn[0]
    assert fqdn == 'tests.modules.withenum.TimeUnit'
    assert umlenum.fqdn == fqdn
    assert umlenum.name == 'TimeUnit'
    members = umlenum.members
    assert len(members) == 3, 'enum has 3 members'
    assert_member(members[0], 'DAYS', 'd')
    assert_member(members[1], 'HOURS', 'h')
    assert_member(members[2], 'MINUTE', 'm')

    assert len(domain_relations) == 0, 'parsing enum adds no relation'

def test_parse_inheritance_within_module():
    domain_items_by_fqdn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    parse_type(GlowingFish, 'tests.modules.withinheritancewithinmodule', domain_items_by_fqdn, domain_relations)

    umlitems_by_fqdn = list(domain_items_by_fqdn.values())
    assert len(umlitems_by_fqdn) == 1, 'the class with multiple inheritance has been parsed'
    child_class: UmlClass = umlitems_by_fqdn[0]
    assert child_class.name == 'GlowingFish'
    assert child_class.fqdn == 'tests.modules.withinheritancewithinmodule.GlowingFish'

    assert len(domain_relations) == 2, '2 inheritance relations must have been parsed'
    inheritance: UmlRelation = domain_relations[0]
    assert inheritance.type == RelType.INHERITANCE
    assert inheritance.source_fqdn == 'tests.modules.withinheritancewithinmodule.Fish', 'parent class'
    assert inheritance.target_fqdn == 'tests.modules.withinheritancewithinmodule.GlowingFish', 'child class'

    inheritance: UmlRelation = domain_relations[1]
    assert inheritance.type == RelType.INHERITANCE
    assert inheritance.source_fqdn == 'tests.modules.withinheritancewithinmodule.Light', 'parent class'
    assert inheritance.target_fqdn == 'tests.modules.withinheritancewithinmodule.GlowingFish', 'child class'

def test_parse_namedtupled_class():
    domain_items_by_fqdn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    parse_type(Circle, 'tests.modules.withnamedtuple', domain_items_by_fqdn, domain_relations)

    umlitems_by_fqdn = list(domain_items_by_fqdn.items())
    assert len(umlitems_by_fqdn) == 1, 'one namedtupled class has been parsed'
    namedtupled_class: UmlClass
    fqdn, namedtupled_class = umlitems_by_fqdn[0]
    assert fqdn == 'tests.modules.withnamedtuple.Circle'
    assert namedtupled_class.fqdn == fqdn
    assert namedtupled_class.name == 'Circle'
    attributes = namedtupled_class.attributes
    assert len(attributes) == 3, 'namedtupled class has 3 attributes'
    assert_attribute(attributes[0], 'x', 'any')
    assert_attribute(attributes[1], 'y', 'any')
    assert_attribute(attributes[2], 'radius', 'any')

    assert len(domain_relations) == 0, 'parsing enum adds no relation'

# from typing import NoneType
from ast import NodeVisitor, arg, FunctionDef, Assign, Attribute, Name, Subscript, get_source_segment
from collections import namedtuple
Argument = namedtuple('Argument', ['id', 'type'])

class ArgumentsCollector(NodeVisitor):
    def __init__(self, constructor_source: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.constructor_source = constructor_source
        self.class_self_id: str = None
        self.arguments: List[Argument] = []

    def visit_arg(self, node: arg):
        if node.annotation is None:
            argument = Argument(node.arg, None)
        elif isinstance(node.annotation, Name):
            argument = Argument(node.arg, None if node.annotation is None else node.annotation.id)
        elif isinstance(node.annotation, Subscript):
            argument = Argument(node.arg, get_source_segment(self.constructor_source, node.annotation))
        else:
            raise ValueError(f'constructor parameter {node.arg} has an annotation of type {type(node.annotation)}, which is not currently handled')

        # first constructor argument is the name for the self reference
        if self.class_self_id is None:
            self.class_self_id = argument.id
        # other arguments are constructor parameters
        else:
            self.arguments.append(argument)

class ConstructorVisitor(NodeVisitor):
    def __init__(self, constructor_source: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.constructor_source = constructor_source
        self.class_self_id: Argument = None
        self.constructor_arguments: List[Argument] = []
        self.uml_attributes: List[UmlAttribute] = []

    def is_constructor_argument(self, argument_id: str) -> bool:
        return any((
            constructor_argument.id == argument_id
            for constructor_argument in self.constructor_arguments
        ))
    def get_constructor_argument(self, argument_id: str) -> Argument:
        return next((
            constructor_argument
            for constructor_argument in self.constructor_arguments
            if constructor_argument.id == argument_id
        ))

    def generic_visit(self, node):
        NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node: FunctionDef):
        # retrieves constructor arguments ('self' reference and typed arguments)
        if node.name == '__init__':
            arguments_collector = ArgumentsCollector(self.constructor_source)
            arguments_collector.visit(node)
            self.class_self_id: str = arguments_collector.class_self_id
            self.constructor_arguments = arguments_collector.arguments
        self.generic_visit(node)

    def visit_Assign(self, node: Assign):
        # recipient of the assignment
        for assigned_target in node.targets:
            # another visitor?
            if isinstance(assigned_target, Attribute) and isinstance(assigned_target.value, Name):
                # the assignment involves an attribute of self
                if assigned_target.value.id == self.class_self_id:
                    # assigned a named variable
                    if isinstance(node.value, Name) and self.is_constructor_argument(node.value.id):
                        self.uml_attributes.append(UmlAttribute(
                            assigned_target.attr, self.get_constructor_argument(node.value.id).type
                        ))
                    else:
                        self.uml_attributes.append(UmlAttribute(assigned_target.attr, None))

def test_parse_constructor():
    from inspect import getsource
    from textwrap import dedent
    point = Point
    constructor_source = getsource(Point.__init__.__code__)
    from ast import parse
    tree = parse(dedent(constructor_source))
    visitor = ConstructorVisitor(dedent(constructor_source))
    visitor.visit(tree)
    print('visitor.class_self_id', visitor.class_self_id)
    print('visitor.constructor_arguments', visitor.constructor_arguments)
    print('visitor.uml_attributes', visitor.uml_attributes)
    assert len(visitor.uml_attributes) == 6
