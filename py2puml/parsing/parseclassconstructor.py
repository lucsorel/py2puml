
from typing import Dict, List, Tuple, Type

from ast import parse, AST
from importlib import import_module
from inspect import getsource
from textwrap import dedent

from py2puml.domain.umlclass import UmlAttribute
from py2puml.domain.umlrelation import UmlRelation
from py2puml.parsing.astvisitors import ConstructorVisitor
from py2puml.parsing.moduleresolver import ModuleResolver

def parse_class_constructor(
    class_type: Type,
    class_fqn: str,
    root_module_name: str
) -> Tuple[List[UmlAttribute], Dict[str, UmlRelation]]:
    constructor = getattr(class_type, '__init__', None)
    # conditions to meet in order to parse the AST of a constructor 
    if (
        # the constructor must be defined
        constructor is None
    ) or (
        # the constructor's source code must be available
        not hasattr(constructor, '__code__')
    ) or (
        # the constructor must belong to the parsed class (not its parent's one)
        constructor.__qualname__ != f'{class_type.__name__}.__init__'
    ):
        return [], {}

    constructor_source: str = dedent(getsource(constructor.__code__))
    constructor_ast: AST = parse(constructor_source)

    module_resolver = ModuleResolver(import_module(class_type.__module__))

    visitor = ConstructorVisitor(constructor_source, class_type.__name__, root_module_name, module_resolver)
    visitor.visit(constructor_ast)

    return visitor.uml_attributes, visitor.uml_relations_by_target_fqn
