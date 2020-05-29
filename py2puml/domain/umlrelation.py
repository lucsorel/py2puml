from dataclasses import dataclass
from enum import Enum

class RelType(Enum):
    COMPOSITION = '*'
    INHERITANCE = '<|'

@dataclass
class UmlRelation(object):
    source_fqdn: str
    target_fqdn: str
    type: RelType
