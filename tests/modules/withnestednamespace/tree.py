from dataclasses import dataclass
from typing import List

from .branches.branch import OakBranch
from .trunks.trunk import Trunk
from .withonlyonesubpackage.underground import Soil
from .withonlyonesubpackage.underground.roots.roots import Roots


@dataclass
class Tree:
    height: float
    roots_depth: float
    roots: Roots
    soil: Soil


@dataclass
class Oak(Tree):
    trunk: Trunk
    branches: List[OakBranch]
