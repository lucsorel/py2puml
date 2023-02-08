from typing import List
from dataclasses import dataclass

from py2puml.domain.umlitem import UmlItem

@dataclass
class UmlAttribute:
    name: str
    type: str
    static: bool

@dataclass
class UmlClass(UmlItem):
    attributes: List[UmlAttribute]
    is_abstract: bool = False
