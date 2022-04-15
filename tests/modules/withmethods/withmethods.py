from __future__ import annotations

from math import pi
from typing import Tuple

from tests import modules
from tests.modules import withenum
from tests.modules.withenum import TimeUnit


class Coordinates:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y


class Point:
    PI: float = pi
    origin = Coordinates(0, 0)

    @staticmethod
    def from_values(x: int, y: str) -> Point:
        return Point(x, y)

    def get_coordinates(self) -> Tuple[float, str]:
        return self.x, self.y

    def __init__(self, x: int, y: Tuple[bool]) -> None:
        self.coordinates: Coordinates = Coordinates(x, float(y))
        self.day_unit: withenum.TimeUnit = withenum.TimeUnit.DAYS
        self.hour_unit: modules.withenum.TimeUnit = modules.withenum.TimeUnit.HOURS
        self.time_resolution: Tuple[str, withenum.TimeUnit] = 'minute', TimeUnit.MINUTE
        self.x = x
        self.y = y

    def do_something(self, posarg_nohint, posarg_hint: str, posarg_default=3) -> int:
        return 44
