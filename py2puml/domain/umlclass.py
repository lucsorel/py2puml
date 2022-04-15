from typing import List
from dataclasses import dataclass

from py2puml.domain.umlitem import UmlItem

@dataclass
class UmlAttribute:
    name: str
    type: str
    static: bool


@dataclass
class UmlMethod(object):
    name: str
    signature: str


@dataclass
class UmlClass(UmlItem):
    attributes: List[UmlAttribute]
    methods: List[UmlMethod]
    is_abstract: bool = False
