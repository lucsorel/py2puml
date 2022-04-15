from dataclasses import dataclass

# the import of the horsepower_to_kilowatt function should not break the parsing
from tests.modules.withsubdomain.subdomain.insubdomain import Engine


@dataclass
class Car:
    name: str
    engine: Engine
