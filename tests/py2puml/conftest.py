"""
Fixtures that can be used by the automated unit tests.

.. code-block:: python

    def test_using_fixtures(domain_items_by_fqn: Dict[str, UmlItem], domain_relations: List[UmlRelation]):
        fqdn = 'tests.modules.withcompoundtypewithdigits'
        inspect_module(import_module(fqdn), fqdn, domain_items_by_fqn, domain_relations)
        assert len(domain_items_by_fqn) == 2, 'two classes must be inspected'
        ...
"""

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
