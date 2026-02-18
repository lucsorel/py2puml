"""This is a package with a __init__.py and a test module only"""

from dataclasses import dataclass


@dataclass
class InInitTest:
    test_member: str
