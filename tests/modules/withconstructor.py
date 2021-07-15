from typing import List, Tuple

from tests.modules import withenum
from tests import modules
from tests.modules.withenum import TimeUnit
import datetime
class Coordinates:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class Point:
    def __init__(self, x: int, y: str, u: float, z: List[int]):
        self.coordinates: Coordinates = Coordinates(x, y)
        self.day_unit: withenum.TimeUnit = withenum.TimeUnit.DAYS
        self.hour_unit: modules.withenum.TimeUnit = modules.withenum.TimeUnit.HOURS
        self.time_resolution: Tuple[str, withenum.TimeUnit] = 'minute', TimeUnit.MINUTE
        z, (r, t) = str(x) + y, ('r', 't')
        print('building')
        self.x = x
        self.y = y
        # type of self.z should be undefined, z has been overridden without type annotation
        self.z = z
        # this assignment should be ignored
        self.z[2]: int = x
        # u param is overridden here (and re-typed), self.w should be float
        u: int = 0
        self.w = u
        # self.u & self.v should at least be found
        self.u, self.v = (1, y)
        # annotated assignment
        self.dates: List[datetime.date] = []
