'''
Fixtures that can be used by the automated unit tests.
'''

from typing import Dict, List

from pytest import fixture

from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlrelation import UmlRelation

@fixture(scope='function')
def domain_items_by_fqn() -> Dict[str, UmlItem]:
    return {}

@fixture(scope='function')
def domain_relations() -> List[UmlRelation]:
    return []
