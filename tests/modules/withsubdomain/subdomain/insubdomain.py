
from dataclasses import dataclass

def horsepower_to_kilowatt(horsepower: float) -> float:
    return horsepower * 745.7

@dataclass
class Engine(object):
    horsepower: int

@dataclass
class Pilot(object):
    name: str
