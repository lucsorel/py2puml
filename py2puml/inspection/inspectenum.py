
from typing import Dict, Type
from enum import Enum

from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlenum import UmlEnum, Member

def inspect_enum_type(
    enum_type: Type[Enum],
    enum_type_fqdn: str,
    domain_items_by_fqdn: Dict[str, UmlItem]
):
    domain_items_by_fqdn[enum_type_fqdn] = UmlEnum(
        name=enum_type.__name__,
        fqdn=enum_type_fqdn,
        members=[
            Member(name=enum_member.name, value=enum_member.value)
            for enum_member in enum_type
        ]
    )
