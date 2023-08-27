from dataclasses import dataclass


# the definition of the horsepower_to_kilowatt function should not break the parsing
def horsepower_to_kilowatt(horsepower: float) -> float:
    return horsepower * 745.7


@dataclass
class Engine:
    horsepower: int


@dataclass
class Pilot:
    name: str
