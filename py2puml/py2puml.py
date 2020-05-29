from typing import Dict, List, Iterable
from types import ModuleType
from pkgutil import walk_packages
from importlib import import_module

from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlrelation import UmlRelation
from py2puml.parser import parse_item_module
from py2puml.exportpuml import to_puml_content


def py2puml(domain_path: str, domain_module: str) -> Iterable[str]:
    domain_items_by_fqdn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    for _, name, is_pkg in walk_packages([domain_path]):
        if not is_pkg:
            domain_item_module: ModuleType = import_module(
                f'{domain_module}.{name}'
            )
            parse_item_module(
                domain_item_module,
                domain_module,
                domain_items_by_fqdn,
                domain_relations
            )
    return to_puml_content(domain_items_by_fqdn.values(), domain_relations)
