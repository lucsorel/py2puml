from py2puml.domain.umlclass import UmlAttribute


def assert_attribute(attribute: UmlAttribute, expected_name: str, expected_type: str, expected_staticity: bool):
    assert attribute.name == expected_name
    assert attribute.type == expected_type
    assert attribute.static == expected_staticity
