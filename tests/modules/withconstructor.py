import datetime
from math import pi
from typing import List, Tuple

from tests import modules
from tests.modules import withenum
from tests.modules.withenum import TimeUnit


class Coordinates:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Point:
    PI: float = pi
    origin = Coordinates(0, 0)

    @staticmethod
    def from_values(x: int, y: str, u: float, z: List[int]) -> 'Point':
        return Point(x, y, u, z)

    def get_coordinates(self):
        return self.x, self.y

    def __init__(self, x: int, y: str, unit: str, u: float, z: List[int]):
        self.coordinates: Coordinates = Coordinates(x, float(y))
        # al the different imports of TimeUnit must be handled and result in the same 'short type' to display
        self.day_unit: withenum.TimeUnit = withenum.TimeUnit.DAYS
        self.hour_unit: modules.withenum.TimeUnit = modules.withenum.TimeUnit.HOURS
        self.time_resolution: Tuple[str, withenum.TimeUnit] = 'minute', TimeUnit.MINUTE
        print('instruction to ignore from parsing')
        if x is not None and y is not None:
            self.x = x
            self.y = y
        # multiple assignments
        self.x_unit = self.y_unit = unit
        # type of self.z should be undefined, z has been overridden without type annotation
        z, (r, t) = str(x) + y, ('r', 't')
        assert r == 'r'
        assert t == 't'
        self.z = z
        # this assignment should be ignored
        self.z[2]: int = x
        # u param is overridden here (and re-typed), self.w must be float
        u: int = 0
        self.w = u
        # tuple definition of self.u & self.v (type annotations are not possible)
        self.u, self.v = (1, y)
        # annotated assignment with compound type
        self.dates: List[datetime.date] = []
