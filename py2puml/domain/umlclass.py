from typing import List
from dataclasses import dataclass

from py2puml.domain.umlitem import UmlItem

@dataclass
class UmlAttribute(object):
    name: str
    type: str
    static: bool

@dataclass
class UmlClass(UmlItem):
    attributes: List[UmlAttribute]
    abstract: bool = False

    @property
    def item_type(self) -> str:
        return 'abstract class' if self.abstract else 'class'
