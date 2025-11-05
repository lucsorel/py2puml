from subprocess import PIPE, run

from pytest import mark

from py2puml.asserts import assert_py2puml_command_args
from py2puml.py2puml import py2puml

from tests import PROJECT_PATH


@mark.parametrize(
    'command',
    [
        'py2puml --path py2puml/domain --namespace py2puml.domain',
        'py2puml --path py2puml/domain',
        'py2puml -p py2puml/domain -n py2puml.domain',
        'py2puml -p py2puml/domain',
        'python -m py2puml --path py2puml/domain --namespace py2puml.domain',
        'python -m py2puml --path py2puml/domain',
        'python -m py2puml -p py2puml/domain -n py2puml.domain',
        'python -m py2puml -p py2puml/domain',
    ],
)
def test_py2puml_with_py2uml_domain(command: str):
    cli_stdout = run(command.split(' '), stdout=PIPE, stderr=PIPE, text=True, check=True).stdout

    puml_content = py2puml('py2puml/domain', 'py2puml.domain')

    assert ''.join(puml_content).strip() == cli_stdout.strip()


def test_assert_domain_documentation():
    assert_py2puml_command_args('-p py2puml/domain', PROJECT_PATH / 'py2puml' / 'py2puml.domain.puml')
