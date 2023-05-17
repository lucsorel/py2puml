from typing import List, Dict
from dataclasses import dataclass, field

from py2puml.domain.umlitem import UmlItem


@dataclass
class UmlAttribute:
    name: str
    type: str
    static: bool

@dataclass
class UmlMethod:
    name: str
    arguments: Dict = field(default_factory=dict)
    is_static: bool = False
    is_class: bool = False
    return_type: str = None

    @property
    def signature(self):
        if self.arguments:
            return ', '.join([f'{arg_type} {arg_name}' for arg_name, arg_type in self.arguments.items()])
        return ''


@dataclass
class UmlClass(UmlItem):
    attributes: List[UmlAttribute]
    methods: List[UmlMethod]
    is_abstract: bool = False
