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
    # forward refs are accounted for
    colleagues: List['Worker']
    boss: 'Worker'
    home_address: Address
    work_address: Address


@dataclass
class Firm:
    name: str
    employees: List[Worker]
