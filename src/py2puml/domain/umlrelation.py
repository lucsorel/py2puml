from dataclasses import dataclass
from enum import Enum, unique


@unique
class RelType(Enum):
    COMPOSITION = '*'
    INHERITANCE = '<|'


@dataclass
class UmlRelation:
    source_fqn: str
    target_fqn: str
    type: RelType
