from typing import List
from dataclasses import dataclass

from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlclass import UmlAttribute

@dataclass
class UmlSubDomainClass(UmlItem):
    attributes: List[UmlAttribute]