
from typing import Dict, Type

from py2puml.domain.umlclass import UmlClass, UmlAttribute
from py2puml.domain.umlitem import UmlItem


def inspect_namedtuple_type(
    namedtuple_type: Type,
    namedtuple_type_fqdn: str,
    domain_items_by_fqdn: Dict[str, UmlItem]
):
    domain_items_by_fqdn[namedtuple_type_fqdn] = UmlClass(
        name=namedtuple_type.__name__,
        fqdn=namedtuple_type_fqdn,
        attributes=[
            UmlAttribute(tuple_field, 'Any')
            for tuple_field in namedtuple_type._fields
        ]
    )
