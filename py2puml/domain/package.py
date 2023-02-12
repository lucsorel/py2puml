from dataclasses import dataclass, field
from typing import List

@dataclass
class Package:
    '''A folder or a python module'''
    name: str
    children: List['Package'] = field(default_factory=list)
    items_number: int = 0
