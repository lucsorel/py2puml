
from dataclasses import dataclass
from typing import List


@dataclass
class Address(object):
    street: str
    zipcode: str
    city: str

@dataclass
class Worker(object):
    name: str
    # forward refs are skipped for now
    colleagues: List['Worker']
    address: Address

@dataclass
class Firm(object):
    name: str
    employees: List[Worker]
