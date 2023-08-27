from dataclasses import dataclass

from tests.modules.withsubdomain.subdomain.insubdomain import Engine


@dataclass
class Car:
    name: str
    engine: Engine
