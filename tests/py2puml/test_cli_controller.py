from pathlib import Path
from subprocess import PIPE, run

from pytest import mark, warns

from py2puml.asserts import assert_py2puml_command_args

from tests import PROJECT_PATH, TEST_MODULES_PATH, __description__, __version__


def test_controller_warns_on_obsolete_positional_args():
    with warns(DeprecationWarning, match='Use `py2puml --path py2puml/domain --namespace py2puml.domain` instead'):
        assert_py2puml_command_args('py2puml/domain py2puml.domain', PROJECT_PATH / 'py2puml' / 'py2puml.domain.puml')


@mark.parametrize('to_output_file', [True, False])
@mark.parametrize(
    ['command_args', 'expected_output_file_path', 'current_working_directory'],
    [
        # ensures that the documentation of the py2puml domain model is up-to-date
        ('--path py2puml/domain --namespace py2puml.domain', PROJECT_PATH / 'py2puml' / 'py2puml.domain.puml', None),
        ('-p py2puml/domain -n py2puml.domain', PROJECT_PATH / 'py2puml' / 'py2puml.domain.puml', None),
        ('-p py2puml/domain', PROJECT_PATH / 'py2puml' / 'py2puml.domain.puml', None),
        # ensures that __init__.py files are also parsed
        (
            '-p tests/modules/withpkginitonly -n tests.modules.withpkginitonly',
            TEST_MODULES_PATH / 'withpkginitonly' / 'tests.modules.withpkginitonly.puml',
            None,
        ),
        # ensures that __init__.py files are also parsed, in combination with other modules
        (
            '-p tests/modules/withpkginitandmodule -n tests.modules.withpkginitandmodule',
            TEST_MODULES_PATH / 'withpkginitandmodule' / 'tests.modules.withpkginitandmodule.puml',
            None,
        ),
        # other use cases
        (
            '-p tests/modules/withnestednamespace -n tests.modules.withnestednamespace',
            TEST_MODULES_PATH / 'withnestednamespace' / 'tests.modules.withnestednamespace.puml',
            None,
        ),
        (
            '-p tests/modules/withsubdomain -n tests.modules.withsubdomain',
            TEST_MODULES_PATH / 'withsubdomain' / 'tests.modules.withsubdomain.puml',
            None,
        ),
        # inspects just a module
        ('-p tests/modules/withenum.py -n tests.modules.withenum', TEST_MODULES_PATH / 'withenum.puml', None),
        # inspects a module with a builtins definition without source code
        (
            '-p tests/modules/withimportedbuiltins.py -n tests.modules.withimportedbuiltins',
            TEST_MODULES_PATH / 'withimportedbuiltins.puml',
            None,
        ),
        # adapts the inspection directory to the parent py2puml directory
        (
            '--path domain --namespace py2puml.domain',
            PROJECT_PATH / 'py2puml' / 'py2puml.domain.puml',
            'py2puml',
        ),
        ('-p withenum.py -n tests.modules.withenum', TEST_MODULES_PATH / 'withenum.puml', 'tests/modules'),
        # adapts the inspection directory to the nested directory
        (
            '-p tests/modules/withrootnotincwd -n withrootnotincwd',
            TEST_MODULES_PATH / 'withrootnotincwd' / 'withrootnotincwd.puml',
            None,
        ),
        ('-p withrootnotincwd', TEST_MODULES_PATH / 'withrootnotincwd' / 'withrootnotincwd.puml', 'tests/modules'),
        (
            '-p tests/modules/withrootnotincwd -n withrootnotincwd',
            TEST_MODULES_PATH / 'withrootnotincwd' / 'withrootnotincwd.puml',
            None,
        ),
        (
            '-p test',
            TEST_MODULES_PATH / 'withconfusingrootpackage' / 'test' / 'test.puml',
            'tests/modules/withconfusingrootpackage',
        ),
        (
            '-p withconfusingrootpackage/test -n test',
            TEST_MODULES_PATH / 'withconfusingrootpackage' / 'test' / 'test.puml',
            'tests/modules',
        ),
    ],
)
def test_controller_stdout_and_in_file(
    tmp_path: Path, to_output_file: bool, command_args, expected_output_file_path: Path, current_working_directory: str
):
    if to_output_file:
        command_args += f' -o {tmp_path / expected_output_file_path.name}'
    assert_py2puml_command_args(command_args, expected_output_file_path, current_working_directory)


@mark.parametrize(
    'version_command',
    [
        'py2puml -v',
        'python -m py2puml -v',
        'py2puml --version',
        'python -m py2puml --version',
    ],
)
def test_controller_version(version_command: str):
    """
    Ensures the consistency between the CLI version and the project version set in pyproject.toml
    which is not included when the CLI is installed system-wise
    """
    cli_version = run(version_command.split(' '), stdout=PIPE, stderr=PIPE, text=True, check=True).stdout

    assert cli_version == f'py2puml {__version__}\n'


@mark.parametrize(
    'help_command',
    [
        'py2puml -h',
        'python -m py2puml -h',
        'py2puml --help',
        'python -m py2puml --help',
    ],
)
def test_controller_help(help_command: str):
    """
    Ensures the consistency between the CLI help and the project description set in pyproject.toml
    which is not included when the CLI is installed system-wise
    """
    help_text = run(help_command.split(' '), stdout=PIPE, stderr=PIPE, text=True, check=True).stdout.replace('\n', ' ')

    assert __description__ in help_text
