from subprocess import run, PIPE
from typing import List

from pytest import mark

from py2puml.py2puml import py2puml
from tests import __version__, __description__

@mark.parametrize(
    'entrypoint', [
        ['py2puml'],
        ['python', '-m', 'py2puml']
    ]
)
def test_cli_consistency_with_the_default_configuration(entrypoint: List[str]):
    command = entrypoint + ['py2puml/domain', 'py2puml.domain']
    cli_stdout = run(command,
        stdout=PIPE, stderr=PIPE,
        text=True, check=True
    ).stdout

    puml_content = py2puml('py2puml/domain', 'py2puml.domain')

    assert ''.join(puml_content).strip() == cli_stdout.strip()

@mark.parametrize(
    'version_command', [
        ['-v'],
        ['--version']
    ]
)
def test_cli_version(version_command: List[str]):
    '''
    Ensures the consistency between the CLI version and the project version set in pyproject.toml
    which is not included when the CLI is installed system-wise
    '''
    command = ['py2puml'] + version_command
    cli_version = run(command,
        stdout=PIPE, stderr=PIPE,
        text=True, check=True
    ).stdout

    assert cli_version == f'py2puml {__version__}\n'

@mark.parametrize(
    'help_command', [
        ['-h'],
        ['--help']
    ]
)
def test_cli_help(help_command: List[str]):
    '''
    Ensures the consistency between the CLI help and the project description set in pyproject.toml
    which is not included when the CLI is installed system-wise
    '''
    command = ['py2puml'] + help_command
    help_text = run(command,
        stdout=PIPE, stderr=PIPE,
        text=True, check=True
    ).stdout.replace('\n', ' ')

    assert __description__ in help_text
