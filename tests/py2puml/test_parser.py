from typing import Dict, List, Tuple

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
from ast import (
    NodeVisitor, arg, expr,
    FunctionDef, Assign, AnnAssign,
    Attribute, Name, Tuple as AstTuple, Subscript, get_source_segment
)
from py2puml.inspection.moduleresolver import ModuleResolver, NamespacedType
from collections import namedtuple
Variable = namedtuple('Variable', ['id', 'type_expr'])

class SignatureVariablesCollector(NodeVisitor):
    '''Collects the variables and their type annotations from the signature of a constructor method'''
    def __init__(self, constructor_source: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.constructor_source = constructor_source
        self.class_self_id: str = None
        self.variables: List[Variable] = []

    def visit_arg(self, node: arg):
        variable = Variable(node.arg, node.annotation)

        # first constructor variable is the name for the 'self' reference
        if self.class_self_id is None:
            self.class_self_id = variable.id
        # other arguments are constructor parameters
        else:
            self.variables.append(variable)

class AssignedVariablesCollector(NodeVisitor):
    def __init__(self, class_self_id: str, annotation: expr, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.class_self_id = class_self_id
        self.annotation = annotation
        self.variables: List[Variable] = []
        self.self_attributes: List[Variable] = []

    def visit_Name(self, node: Name):
        '''
        Detects declarations of new variables
        '''
        if node.id != self.class_self_id:
            self.variables.append(Variable(node.id, self.annotation))

    def visit_Attribute(self, node: Attribute):
        '''
        Detects declarations of new attribute on 'self'
        '''
        if isinstance(node.value, Name) and node.value.id == self.class_self_id:
            self.self_attributes.append(Variable(node.attr, self.annotation))

    def generic_visit(self, node):
        NodeVisitor.generic_visit(self, node)

class ConstructorVisitor(NodeVisitor):
    '''Identifies the assignments done to self in the body of a constructor method'''
    def __init__(self, constructor_source: str, class_name: str, module_resolver: ModuleResolver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.constructor_source = constructor_source
        self.class_name = class_name
        self.module_resolver = module_resolver
        self.class_self_id: str = None
        self.variables_namespace: List[Variable] = []
        self.uml_attributes: List[UmlAttribute] = []
        self.uml_relations: List[UmlRelation] = []

    def is_in_variables_namespace(self, variable_id: str) -> bool:
        return get_from_namespace(variable_id) == None

    def get_from_namespace(self, variable_id: str) -> Variable:
        return next((
            variable
            # variables namespace is iterated antichronologically
            # to account for variables being overridden
            for variable in self.variables_namespace[::-1]
            if variable.id == variable_id
        ), None)

    def generic_visit(self, node):
        NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node: FunctionDef):
        # retrieves constructor arguments ('self' reference and typed arguments)
        if node.name == '__init__':
            variables_collector = SignatureVariablesCollector(self.constructor_source)
            variables_collector.visit(node)
            self.class_self_id: str = variables_collector.class_self_id
            self.variables_namespace = variables_collector.variables

        self.generic_visit(node)

    def visit_AnnAssign(self, node: AnnAssign):
        variables_collector = AssignedVariablesCollector(self.class_self_id, node.annotation)
        variables_collector.visit(node.target)

        short_type, full_namespaced_definitions = self.derive_type_annotation_details(node.annotation)
        # if any, there is at most one self-assignment
        for variable in variables_collector.self_attributes:
            self.uml_attributes.append(UmlAttribute(variable.id, short_type))
            # TODO process full_namespaced_definitions into relationships

        # if any, there is at most one typed variable added to the scope
        self.variables_namespace.extend(variables_collector.variables)

    def visit_Assign(self, node: Assign):
        # recipients of the assignment
        for assigned_target in node.targets:
            variables_collector = AssignedVariablesCollector(self.class_self_id, None)
            variables_collector.visit(assigned_target)

            # attempts to infer attribute type when a single attribute is assigned to a variable
            if (
                len(variables_collector.self_attributes) == 1
            ) and (
                isinstance(node.value, Name)
            ) and (
                self.is_in_variables_namespace(node.value.id)
            ):
                assigned_variable = self.get_from_namespace(node.value.id)
                short_type, full_namespaced_definitions = self.derive_type_annotation_details(
                    assigned_variable.type_expr
                )
                self.uml_attributes.append(UmlAttribute(assigned_variable.id, short_type))
                # TODO handle relationships with full_namespaced_definitions

            else:
                for variable in variables_collector.self_attributes:
                    self.uml_attributes.append(UmlAttribute(variable.id, None))

            self.variables_namespace.extend(variables_collector.variables)

    def derive_type_annotation_details(self, annotation: expr) -> Tuple[str, List[str]]:
        '''
        From a type annotation
        - a short version of the type (withenum.TimeUnit -> TimeUnit, Tuple[withenum.TimeUnit] -> Tuple[TimeUnit])
        - a list of the full-namespaced definitions involved in the type annotation (in order to build the relationships)
        '''
        if annotation is None:
            return None, []

        # annotation: primitive type, object definition
        if isinstance(annotation, Name):
            full_namespaced_type, short_type = self.module_resolver.resolve_full_namespace_type(
                annotation.id
            )
            return short_type, [full_namespaced_type]
        # annotation: definition from module
        elif isinstance(annotation, Attribute):
            full_namespaced_type, short_type = self.module_resolver.resolve_full_namespace_type(
                get_source_segment(self.constructor_source, annotation)
            )
            return short_type, [full_namespaced_type]
        # annotation: compound type (List[...], Dict, Tuple)
        elif isinstance(annotation, Subscript):
            complex_type = get_source_segment(self.constructor_source, annotation)
            print('need to handle (and shorten)', complex_type)
            # TODO:
            # - regexp to extract assignments
            # - infer the full namespaced types
            # - from types extracted from the source code, replace by the types as they were regexped by their short name
            assignment_types = []
            return complex_type, []

        return None, []


def test_parse_constructor():
    from inspect import getsource
    from textwrap import dedent
    constructor_source = getsource(Point.__init__.__code__)
    from ast import parse
    tree = parse(dedent(constructor_source))

    from importlib import import_module
    class_module = import_module(Point.__module__)
    module_resolver = ModuleResolver(class_module)

    visitor = ConstructorVisitor(dedent(constructor_source), Point.__name__, module_resolver)
    visitor.visit(tree)
    print('visitor.class_self_id', visitor.class_self_id)
    print('visitor.variables_namespace', visitor.variables_namespace)
    print('visitor.uml_attributes', visitor.uml_attributes)
    # print(hasattr(class_module, 'Coordinates'))
    # print(class_module.Coordinates.__module__)
    # print(class_module.modules.withenum.TimeUnit.__module__)
    # print(class_module.withenum.TimeUnit.__module__)
    assert len(visitor.uml_attributes) == 10
