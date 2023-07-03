from py2puml.domain.umlrelation import RelType, UmlRelation


def assert_relation(uml_relation: UmlRelation, source_fqn: str, target_fqn: str, rel_type: RelType):
    assert uml_relation.source_fqn == source_fqn, 'source end'
    assert uml_relation.target_fqn == target_fqn, 'target end'
    assert uml_relation.type == rel_type
