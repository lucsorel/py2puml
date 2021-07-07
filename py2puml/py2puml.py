from pkgutil import iter_modules
from types import ModuleType
from typing import Dict, Iterable, List, Union

from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlrelation import UmlRelation
from py2puml.exportpuml import to_puml_content
from py2puml.parser import parse_item_module


def py2puml(domain_path: str, domain_module: Union[str, None]) -> Iterable[str]:
    domain_items_by_fqdn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []

    found_packages = iter_modules([domain_path], prefix=f"{domain_module}.")
    for importer, name, is_pkg in found_packages:
        if not is_pkg:
            domain_item_module: ModuleType = importer.find_module(name).load_module(name)
            parse_item_module(
                domain_item_module,
                domain_module,
                domain_items_by_fqdn,
                domain_relations,
            )
    return to_puml_content(domain_items_by_fqdn.values(), domain_relations)
