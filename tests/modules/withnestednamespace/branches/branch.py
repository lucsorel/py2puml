from dataclasses import dataclass
from typing import List

from ..nomoduleroot.modulechild.leaf import OakLeaf


@dataclass
class Branch:
    length: float


@dataclass
class OakBranch(Branch):
    sub_branches: List['OakBranch']
    leaves: List[OakLeaf]
