from typing import Dict, List, NamedTuple

from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlrelation import UmlRelation


class Inspection(NamedTuple):
    items_by_fqn: Dict[str, UmlItem]
    relations: List[UmlRelation]
