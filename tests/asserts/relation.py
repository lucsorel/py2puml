
from py2puml.domain.umlrelation import UmlRelation, RelType

def assert_relation(uml_relation: UmlRelation, source_fqdn: str, target_fqdn: str, rel_type: RelType):
    assert uml_relation.source_fqdn == source_fqdn, 'source end'
    assert uml_relation.target_fqdn == target_fqdn, 'target end'
    assert uml_relation.type == rel_type