from .withmethods import Point


class ThreeDimensionalPoint(Point):
    def __init__(self, x: int, y: str, z: float):
        super().__init__(x=x, y=y)
        self.z = z

    def move(self, offset: int):
        self.x += offset

    def check_positive(self) -> bool:
        return self.x > 0
