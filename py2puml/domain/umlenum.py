from typing import List
from dataclasses import dataclass

from py2puml.domain.umlitem import UmlItem

@dataclass
class Member(object):
    name: str
    value: str

@dataclass
class UmlEnum(UmlItem):
    members: List[Member]
