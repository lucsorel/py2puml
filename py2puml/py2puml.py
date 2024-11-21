from typing import Dict, Iterable, List, Optional

from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlrelation import UmlRelation
from py2puml.export.puml import Filters, to_puml_content
from py2puml.inspection.inspectpackage import inspect_package


def py2puml(domain_path: str, domain_module: str, filters: Optional[Filters] = None) -> Iterable[str]:
    domain_items_by_fqn: Dict[str, UmlItem] = {}
    domain_relations: List[UmlRelation] = []
    inspect_package(domain_path, domain_module, domain_items_by_fqn, domain_relations)

    return to_puml_content(domain_module, domain_items_by_fqn.values(), domain_relations, filters)
