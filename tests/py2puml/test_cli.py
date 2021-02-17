
from pytest import mark
from subprocess import run, PIPE

from py2puml import py2puml

@mark.parametrize(
    'entrypoint', [
        ['py2puml'],
        ['python', '-m', 'py2puml']
    ]
)
def test_cli_consistency_with_the_default_configuration(entrypoint):
    command = entrypoint + ['py2puml/domain', 'py2puml.domain']
    cli_stdout = run(command,
        stdout=PIPE, stderr=PIPE,
        text=True, check=True
    ).stdout

    puml_content = py2puml.py2puml('py2puml/domain', 'py2puml.domain')

    assert ''.join(puml_content).strip() == cli_stdout.strip()
