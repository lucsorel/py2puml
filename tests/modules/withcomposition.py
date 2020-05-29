from typing import List, ForwardRef

class Address(object):
    street: str
    zipcode: str
    city: str

class Worker(object):
    name: str
    # forward refs are skipped for now
    colleagues: List['Worker']
    address: Address

class Firm(object):
    name: str
    employees: List[Worker]
