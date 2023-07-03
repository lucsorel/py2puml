from importlib import import_module
from pkgutil import walk_packages
from types import ModuleType
from typing import Dict, List

from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlrelation import UmlRelation
from py2puml.inspection.inspectmodule import inspect_module


def inspect_package(
    domain_path: str, domain_module: str, domain_items_by_fqn: Dict[str, UmlItem], domain_relations: List[UmlRelation]
):
    for _, name, is_pkg in walk_packages([domain_path], f'{domain_module}.'):
        if not is_pkg:
            domain_item_module: ModuleType = import_module(name)
            inspect_module(domain_item_module, domain_module, domain_items_by_fqn, domain_relations)
