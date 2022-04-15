from ast import AnnAssign, Assign, Attribute, FunctionDef, Name, NodeVisitor, Subscript, arg, expr, get_source_segment
from collections import namedtuple
from typing import Dict, List, Tuple, Type

from py2puml.domain.umlclass import UmlAttribute, UmlMethod
from py2puml.domain.umlrelation import RelType, UmlRelation
from py2puml.parsing.compoundtypesplitter import SPLITTING_CHARACTERS, CompoundTypeSplitter
from py2puml.parsing.moduleresolver import ModuleResolver

Argument = namedtuple('Argument', ['id', 'type_expr'])


class SignatureArgumentsCollector(NodeVisitor):
    """
    Collects the arguments name and type annotations from the signature of a method
    """

    def __init__(self, skip_self=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skip_self = skip_self
        self.class_self_id: str = None
        self.arguments: List[Argument] = []
        self.datatypes = {}

    def visit_arg(self, node: arg):
        argument = Argument(node.arg, node.annotation)
        if node.annotation:
            type_visitor = TypeVisitor()
            datatype = type_visitor.visit(node.annotation)
        else:
            datatype = None
        self.datatypes[node.arg] = datatype
        # first constructor argument is the name for the 'self' reference
        if self.class_self_id is None and not self.skip_self:
            self.class_self_id = argument.id
        # other arguments are constructor parameters
        self.arguments.append(argument)


class AssignedVariablesCollector(NodeVisitor):
    """Parses the target of an assignment statement to detect whether the value is assigned to a variable or an instance attribute"""

    def __init__(self, class_self_id: str, annotation: expr):
        self.class_self_id: str = class_self_id
        self.annotation: expr = annotation
        self.variables: List[Argument] = []
        self.self_attributes: List[Argument] = []

    def visit_Name(self, node: Name):
        """
        Detects declarations of new variables
        """
        if node.id != self.class_self_id:
            self.variables.append(Argument(node.id, self.annotation))

    def visit_Attribute(self, node: Attribute):
        """
        Detects declarations of new attributes on 'self'
        """
        if isinstance(node.value, Name) and node.value.id == self.class_self_id:
            self.self_attributes.append(Argument(node.attr, self.annotation))

    def visit_Subscript(self, node: Subscript):
        """
        Assigns a value to a subscript of an existing variable: must be skipped
        """
        pass


class ClassVisitor(NodeVisitor):
    def __init__(self, class_type: Type, root_fqn: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uml_methods: List[UmlMethod] = []

    def visit_FunctionDef(self, node: FunctionDef):
        method_visitor = MethodVisitor()
        method_visitor.visit(node)
        self.uml_methods.append(method_visitor.uml_method)


class TypeVisitor(NodeVisitor):
    """Returns a string representation of a data type. Supports nested compound data types"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def visit_Name(self, node):
        return node.id

    def visit_Constant(self, node):
        return node.value

    def visit_Subscript(self, node: Subscript):
        """Visit node of type ast.Subscript and returns a string representation of the compound datatype. Iterate
        over elements contained in slice attribute by calling recursively visit() method of new instances of
        TypeVisitor. This allows to resolve nested compound datatype."""

        datatypes = []

        if hasattr(node.slice.value, 'elts'):
            for child_node in node.slice.value.elts:
                child_visitor = TypeVisitor()
                datatypes.append(child_visitor.visit(child_node))
        else:
            child_visitor = TypeVisitor()
            datatypes.append(child_visitor.visit(node.slice.value))

        joined_datatypes = ', '.join(datatypes)

        return f'{node.value.id}[{joined_datatypes}]'


class MethodVisitor(NodeVisitor):
    """
    Node visitor subclass used to walk the abstract syntax tree of a method class and identify method arguments.

    If the method is the class constructor, instance attributes (and their type) are also identified by looking both at the constructor signature and constructor's body. When searching in the constructor's body, the visitor looks for relevant assignments (with and without type annotation).
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variables_namespace: List[Argument] = []
        self.uml_method: UmlMethod

    def visit_FunctionDef(self, node: FunctionDef):
        decorators = [decorator.id for decorator in node.decorator_list]
        is_static = 'staticmethod' in decorators
        is_class = 'classmethod' in decorators
        arguments_collector = SignatureArgumentsCollector(skip_self=is_static)
        arguments_collector.visit(node)
        self.variables_namespace = arguments_collector.arguments

        self.uml_method = UmlMethod(name=node.name, is_static=is_static, is_class=is_class)

        for argument in arguments_collector.arguments:
            if argument.id == arguments_collector.class_self_id:
                self.uml_method.arguments[argument.id] = None
            if argument.type_expr:
                if hasattr(argument.type_expr, 'id'):
                    self.uml_method.arguments[argument.id] = argument.type_expr.id
                else:
                    self.uml_method.arguments[argument.id] = arguments_collector.datatypes[argument.id]
            else:
                self.uml_method.arguments[argument.id] = None

        if node.returns is not None:
            return_visitor = TypeVisitor()
            self.uml_method.return_type = return_visitor.visit(node.returns)


class ConstructorVisitor(NodeVisitor):
    """
    Identifies the attributes (and infer their type) assigned to self in the body of a constructor method
    """

    def __init__(
        self,
        constructor_source: str,
        class_name: str,
        root_fqn: str,
        module_resolver: ModuleResolver,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.constructor_source = constructor_source
        self.class_fqn: str = f'{module_resolver.module.__name__}.{class_name}'
        self.root_fqn = root_fqn
        self.module_resolver = module_resolver
        self.class_self_id: str
        self.variables_namespace: List[Argument] = []
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

    def get_from_namespace(self, variable_id: str) -> Argument:
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
            variables_collector = SignatureArgumentsCollector()
            variables_collector.visit(node)
            self.class_self_id: str = variables_collector.class_self_id
            self.variables_namespace = variables_collector.arguments

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
                    (
                        short_type,
                        full_namespaced_definitions,
                    ) = self.derive_type_annotation_details(assigned_variable.type_expr)
                    self.uml_attributes.append(
                        UmlAttribute(variables_collector.self_attributes[0].id, short_type, False)
                    )
                    self.extend_relations(full_namespaced_definitions)

            else:
                for variable in variables_collector.self_attributes:
                    (
                        short_type,
                        full_namespaced_definitions,
                    ) = self.derive_type_annotation_details(variable.type_expr)
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
            (
                full_namespaced_type,
                short_type,
            ) = self.module_resolver.resolve_full_namespace_type(annotation.id)
            return short_type, [full_namespaced_type]
        # definition from module
        elif isinstance(annotation, Attribute):
            (
                full_namespaced_type,
                short_type,
            ) = self.module_resolver.resolve_full_namespace_type(
                get_source_segment(self.constructor_source, annotation)
            )
            return short_type, [full_namespaced_type]
        # compound type (List[...], Tuple[Dict[str, float], module.DomainType], etc.)
        elif isinstance(annotation, Subscript):
            source_segment = get_source_segment(self.constructor_source, annotation)
            short_type, associated_types = shorten_compound_type_annotation(source_segment, self.module_resolver)
            return short_type, associated_types
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
        # characters like '[', ']', ','
        if compound_type_part in SPLITTING_CHARACTERS:
            compound_short_type_parts.append(compound_type_part)
            if compound_type_part == ',':
                compound_short_type_parts.append(' ')
        # replaces each type definition by its short class name
        else:
            (
                full_namespaced_type,
                short_type,
            ) = module_resolver.resolve_full_namespace_type(compound_type_part)
            if short_type is None:
                raise ValueError(
                    f'Could not resolve type {compound_type_part} in module {module_resolver.module}: it needs to be imported explicitely.'
                )
            else:
                compound_short_type_parts.append(short_type)
            associated_types.append(full_namespaced_type)

    return ''.join(compound_short_type_parts), associated_types
