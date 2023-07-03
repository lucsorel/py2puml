from dataclasses import dataclass


@dataclass
class Contact:
    full_name: str
    age: int
    weight: float
    can_twist_tongue: bool
