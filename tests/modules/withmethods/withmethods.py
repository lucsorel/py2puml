from typing import List, Tuple
from math import pi

from tests.modules import withenum
from tests import modules
from tests.modules.withenum import TimeUnit


class Coordinates:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Point:
    PI: float = pi
    origin = Coordinates(0, 0)

    @staticmethod
    def from_values(x: int, y: str, u: float) -> 'Point':
        return Point(x, y, u)

    def get_coordinates(self):
        return self.x, self.y

    def __init__(self, x: int, y: str):
        self.coordinates: Coordinates = Coordinates(x, float(y))
        self.day_unit: withenum.TimeUnit = withenum.TimeUnit.DAYS
        self.hour_unit: modules.withenum.TimeUnit = modules.withenum.TimeUnit.HOURS
        self.time_resolution: Tuple[str, withenum.TimeUnit] = 'minute', TimeUnit.MINUTE
        self.x = x
        self.y = y
