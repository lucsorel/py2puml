from pathlib import Path

from pytest import raises

from py2puml.controller import InspectorController


def test_inspectorcontroller_check_domain_path_and_namespace_consistency_with_valid_args():
    assert InspectorController()._check_domain_path_and_namespace_consistency(
        Path('src') / 'py2puml' / 'domain', 'py2puml.domain'
    ) == Path('src')


def test_inspectorcontroller_check_domain_path_and_namespace_consistency_with_invalid_args():
    with raises(ValueError) as error:
        InspectorController()._check_domain_path_and_namespace_consistency(
            Path('src') / 'py2puml' / 'domain' / 'umlitem', 'py2puml.umlitem'
        )

    assert (
        str(error.value)
        == "the namespace part 'py2puml' of namespace 'py2puml.umlitem' does not match subpath 'src/py2puml/domain' of 'src/py2puml/domain/umlitem'"
    )
