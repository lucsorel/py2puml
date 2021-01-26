# the import of the horsepower_to_kilowatt function should not break the parsing
from tests.modules.withsubdomain.subdomain.insubdomain import Engine, horsepower_to_kilowatt

class Car(object):
    name: str
    engine: Engine
