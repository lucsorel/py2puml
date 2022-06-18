
from dataclasses import dataclass
from typing import List


@dataclass
class Address:
    street: str
    zipcode: str
    city: str

@dataclass
class Worker:
    name: str
    # forward refs are skipped for now
    colleagues: List['Worker']
    address: Address

@dataclass
class Firm:
    name: str
    employees: List[Worker]
