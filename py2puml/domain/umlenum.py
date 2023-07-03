from dataclasses import dataclass
from typing import List

from py2puml.domain.umlitem import UmlItem


@dataclass
class Member:
    name: str
    value: str


@dataclass
class UmlEnum(UmlItem):
    members: List[Member]
