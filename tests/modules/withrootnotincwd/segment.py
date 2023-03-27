from dataclasses import dataclass

from withrootnotincwd.point import Point


@dataclass
class Segment:
    a: Point
    b: Point
