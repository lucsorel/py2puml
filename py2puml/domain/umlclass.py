from typing import List
from dataclasses import dataclass

from py2puml.domain.umlitem import UmlItem

@dataclass
class UmlAttribute(object):
    name: str
    type: str

@dataclass
class UmlClass(UmlItem):
    attributes: List[UmlAttribute]
