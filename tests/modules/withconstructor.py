from typing import List

from tests.modules import withenum
from tests import modules
from tests.modules.withenum import TimeUnit
import datetime
class Coordinates:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class Point:
    def __init__(self, x: int, y: str, z: List[int]):
        self.coordinates: Coordinates = Coordinates(x, y)
        self.day_unit: withenum.TimeUnit = withenum.TimeUnit.DAYS
        self.hour_unit: modules.withenum.TimeUnit = modules.withenum.TimeUnit.HOURS
        self.time_resolution: Tuple[str, TimeUnit] = 'minute', TimeUnit.MINUTE
        z = str(x) + y
        print('building')
        self.x = x
        self.y = y
        # type of self.z should be deduced from its annotation
        self.z: str = z
        # this assignment should be ignored
        self.z[2] = x
        # it would be great to have self.w typed as int
        u: int = 0
        self.w = u
        # self.u & self.v should at least be found
        self.u, self.v = (1, y)
        # annotated assignment
        self.dates: List[datetime.date] = []
