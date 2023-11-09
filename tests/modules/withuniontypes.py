from dataclasses import dataclass
from typing import Union


@dataclass
class NumberWrapper:
    number: Union[int, float]


@dataclass
class OptionalNumberWrapper:
    number: Union[int, float, None]


@dataclass
class NumberWrapperPy3_10:
    number: int | float


@dataclass
class OptionalNumberWrapperPy3_10:
    number: int | float | None


class DistanceCalculator:
    def __init__(
        self,
        x_a: Union[int, float],
        y_a: Union[int, float, None],
        x_b: int | float,
        y_b: int | float | None,
        euclidian: bool = True,
    ):
        self.x_a = x_a
        self.y_a = y_a
        self.x_b = x_b
        self.y_b = y_b
        space_characs: str | None = 'euclidian space' if euclidian else None
        self.space_characs = space_characs
