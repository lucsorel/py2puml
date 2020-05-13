from typing import List
from dataclasses import dataclass

from py2puml.domain.umlattribute import UmlAttribute

@dataclass
class UmlClass(object):
    name: str
    fqdn: str
    attributes: List[UmlAttribute]
