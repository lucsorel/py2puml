"""This is a package with a __init__.py file only"""

from dataclasses import dataclass


@dataclass
class InInitTest:
    test_member: str
