
def horsepower_to_kilowatt(horsepower: float) -> float:
    return horsepower * 745.7

class Engine(object):
    horsepower: int

class Pilot(object):
    name: str
