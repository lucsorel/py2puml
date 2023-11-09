from io import StringIO
from pathlib import Path
from typing import Iterable, List, Union

from py2puml.py2puml import py2puml


def assert_py2puml_is_file_content(domain_path: str, domain_module: str, diagram_filepath: Union[str, Path]):
    # reads the existing class diagram
    with open(diagram_filepath, 'r', encoding='utf8') as expected_puml_file:
        assert_py2puml_is_stringio(domain_path, domain_module, expected_puml_file)


def normalize_lines_with_returns(lines_with_returns: Iterable[str]) -> List[str]:
    """
    When comparing contents, each piece of contents can either be:
    - a formatted string block output by the py2puml command containg line returns
    - a single line of contents read from a file, each line ending with a line return

    This function normalizes each sequence of contents as a list of string lines,
    each one finishing without a line return to ease comparison.
    """
    return ''.join(lines_with_returns).split('\n')


def assert_py2puml_is_stringio(domain_path: str, domain_module: str, expected_content_stream: StringIO):
    puml_content_lines = normalize_lines_with_returns(py2puml(domain_path, domain_module))
    expected_content_lines = normalize_lines_with_returns(expected_content_stream)

    assert_multilines(puml_content_lines, expected_content_lines)


def assert_multilines(actual_multilines: List[str], expected_multilines: List[str]):
    line_index = 0
    for line_index, (actual_line, expected_line) in enumerate(zip(actual_multilines, expected_multilines)):
        # print(f'{actual_line=}\n{expected_line=}')
        assert (
            actual_line == expected_line
        ), f'actual and expected contents have changed at line {line_index + 1}: {actual_line=}, {expected_line=}'

    assert line_index + 1 == len(actual_multilines), f'actual and expected diagrams have {line_index + 1} lines'
