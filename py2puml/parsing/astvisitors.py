from ast import (
    AnnAssign,
    Assign,
    Attribute,
    BinOp,
    FunctionDef,
    Name,
    NodeVisitor,
    Subscript,
    arg,
    expr,
    get_source_segment,
)
from collections import namedtuple
from typing import Dict, List, Tuple

from py2puml.domain.umlclass import UmlAttribute
from py2puml.domain.umlrelation import RelType, UmlRelation
from py2puml.parsing.compoundtypesplitter import SPLITTING_CHARACTERS, CompoundTypeSplitter
from py2puml.parsing.moduleresolver import ModuleResolver

Variable = namedtuple('Variable', ['id', 'type_expr'])


class SignatureVariablesCollector(NodeVisitor):
    """
    Collects the variables and their type annotations from the signature of a constructor method
    """

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
    """Parses the target of an assignment statement to detect whether the value is assigned to a variable or an instance attribute"""

    def __init__(self, class_self_id: str, annotation: expr):
        self.class_self_id: str = class_self_id
        self.annotation: expr = annotation
        self.variables: List[Variable] = []
        self.self_attributes: List[Variable] = []

    def visit_Name(self, node: Name):
        """
        Detects declarations of new variables
        """
        if node.id != self.class_self_id:
            self.variables.append(Variable(node.id, self.annotation))

    def visit_Attribute(self, node: Attribute):
        """
        Detects declarations of new attributes on 'self'
        """
        if isinstance(node.value, Name) and node.value.id == self.class_self_id:
            self.self_attributes.append(Variable(node.attr, self.annotation))

    def visit_Subscript(self, node: Subscript):
        """
        Assigns a value to a subscript of an existing variable: must be skipped
        """
        pass


class ConstructorVisitor(NodeVisitor):
    """
    Identifies the attributes (and infer their type) assigned to self in the body of a constructor method
    """

    def __init__(
        self, constructor_source: str, class_name: str, root_fqn: str, module_resolver: ModuleResolver, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.constructor_source = constructor_source
        self.class_fqn: str = f'{module_resolver.module.__name__}.{class_name}'
        self.root_fqn = root_fqn
        self.module_resolver = module_resolver
        self.class_self_id: str
        self.variables_namespace: List[Variable] = []
        self.uml_attributes: List[UmlAttribute] = []
        self.uml_relations_by_target_fqn: Dict[str, UmlRelation] = {}

    def extend_relations(self, target_fqns: List[str]):
        self.uml_relations_by_target_fqn.update(
            {
                target_fqn: UmlRelation(self.class_fqn, target_fqn, RelType.COMPOSITION)
                for target_fqn in target_fqns
                if target_fqn.startswith(self.root_fqn) and (target_fqn not in self.uml_relations_by_target_fqn)
            }
        )

    def get_from_namespace(self, variable_id: str) -> Variable:
        return next(
            (
                variable
                # variables namespace is iterated antichronologically
                # to account for variables being overridden
                for variable in self.variables_namespace[::-1]
                if variable.id == variable_id
            ),
            None,
        )

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
            self.uml_attributes.append(UmlAttribute(variable.id, short_type, static=False))
            self.extend_relations(full_namespaced_definitions)

        # if any, there is at most one typed variable added to the scope
        self.variables_namespace.extend(variables_collector.variables)

    def visit_Assign(self, node: Assign):
        # recipients of the assignment
        for assigned_target in node.targets:
            variables_collector = AssignedVariablesCollector(self.class_self_id, None)
            variables_collector.visit(assigned_target)

            # attempts to infer attribute type when a single attribute is assigned to a variable
            if (len(variables_collector.self_attributes) == 1) and (isinstance(node.value, Name)):
                assigned_variable = self.get_from_namespace(node.value.id)
                if assigned_variable is not None:
                    short_type, full_namespaced_definitions = self.derive_type_annotation_details(
                        assigned_variable.type_expr
                    )
                    self.uml_attributes.append(
                        UmlAttribute(variables_collector.self_attributes[0].id, short_type, False)
                    )
                    self.extend_relations(full_namespaced_definitions)

            else:
                for variable in variables_collector.self_attributes:
                    short_type, full_namespaced_definitions = self.derive_type_annotation_details(variable.type_expr)
                    self.uml_attributes.append(UmlAttribute(variable.id, short_type, static=False))
                    self.extend_relations(full_namespaced_definitions)

            # other assignments were done in new variables that can shadow existing ones
            self.variables_namespace.extend(variables_collector.variables)

    def derive_type_annotation_details(self, annotation: expr) -> Tuple[str, List[str]]:
        """
        From a type annotation, derives:
        - a short version of the type (withenum.TimeUnit -> TimeUnit, Tuple[withenum.TimeUnit] -> Tuple[TimeUnit])
        - a list of the full-namespaced definitions involved in the type annotation (in order to build the relationships)
        """
        if annotation is None:
            return None, []

        # primitive type, object definition
        if isinstance(annotation, Name):
            full_namespaced_type, short_type = self.module_resolver.resolve_full_namespace_type(annotation.id)
            return short_type, [full_namespaced_type]
        # definition from module
        elif isinstance(annotation, Attribute):
            full_namespaced_type, short_type = self.module_resolver.resolve_full_namespace_type(
                get_source_segment(self.constructor_source, annotation)
            )
            return short_type, [full_namespaced_type]
        # compound type (List[...], Tuple[Dict[str, float], module.DomainType], etc.) or '|'-based union type
        elif isinstance(annotation, (Subscript, BinOp)):
            return shorten_compound_type_annotation(
                get_source_segment(self.constructor_source, annotation), self.module_resolver
            )

        return None, []


def shorten_compound_type_annotation(type_annotation: str, module_resolver: ModuleResolver) -> Tuple[str, List[str]]:
    """
    In the string representation of a compound type annotation, the elementary types can be prefixed by their packages or sub-packages.
    Like in 'Dict[datetime.datetime,typing.List[Worker]]'. This function returns a tuple of 2 values:
    - a string representation with shortened types for display purposes in the PlantUML documentation: 'Dict[datetime, List[Worker]]'
      (note: a space is inserted after each coma for readability sake)
    - a list of the fully-qualified types involved in the annotation: ['typing.Dict', 'datetime.datetime', 'typing.List', 'mymodule.Worker']
    """
    compound_type_parts: List[str] = CompoundTypeSplitter(type_annotation, module_resolver.module.__name__).get_parts()
    compound_short_type_parts: List[str] = []
    associated_types: List[str] = []
    for compound_type_part in compound_type_parts:
        # characters like '[', ']', ',', '|'
        if compound_type_part in SPLITTING_CHARACTERS:
            if compound_type_part == ',':
                compound_short_type_parts.append(', ')
            elif compound_type_part == '|':
                compound_short_type_parts.append(' | ')
            else:
                compound_short_type_parts.append(compound_type_part)
        # replaces each type definition by its short class name
        else:
            full_namespaced_type, short_type = module_resolver.resolve_full_namespace_type(compound_type_part)
            if short_type is None:
                raise ValueError(
                    f'Could not resolve type {compound_type_part} in module {module_resolver.module}: it needs to be imported explicitly.'
                )
            else:
                compound_short_type_parts.append(short_type)
            associated_types.append(full_namespaced_type)

    return ''.join(compound_short_type_parts), associated_types
