from py2puml.domain.umlclass import UmlMethod


def assert_method(method: UmlMethod, expected_name: str, expected_signature: str):
    assert method.name == expected_name
    assert method.signature == expected_signature
    # TODO: add 'is_static' attribute to UmlMethod for static methods
    # TODO: add 'is_class' attribute to UmlMethod for class methods
