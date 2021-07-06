from typing import List

class Point:
    def __init__(self, x: int, y: str, z: List[int]):
        z = str(x) + y
        print('building')
        self.x = x
        self.y = y
        self.z = z
        # this should be ignored
        self.z[2] = x
        # it would be great to have self.w typed as int
        u: int = 0
        self.w = u
        # self.u & self.v should at least be found
        self.u, self.v = (1, y)