from typing import Dict, Type

from py2puml.domain.umlclass import UmlAttribute, UmlClass
from py2puml.domain.umlitem import UmlItem


def inspect_namedtuple_type(namedtuple_type: Type, namedtuple_type_fqn: str, domain_items_by_fqn: Dict[str, UmlItem]):
    domain_items_by_fqn[namedtuple_type_fqn] = UmlClass(
        name=namedtuple_type.__name__,
        fqn=namedtuple_type_fqn,
        attributes=[UmlAttribute(tuple_field, 'Any', False) for tuple_field in namedtuple_type._fields],
    )
