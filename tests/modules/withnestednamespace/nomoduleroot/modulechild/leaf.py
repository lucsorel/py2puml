from dataclasses import dataclass


@dataclass
class CommownLeaf:
    color: int
    area: float


@dataclass
class PineLeaf(CommownLeaf):
    length: float


@dataclass
class OakLeaf(CommownLeaf):
    curves: int
