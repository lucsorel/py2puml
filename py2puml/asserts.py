from io import StringIO
from pathlib import Path
from typing import Iterable, List, Union

from py2puml.py2puml import py2puml


def assert_py2puml_is_file_content(domain_path: str, domain_module: str, diagram_filepath: Union[str, Path]):
    # reads the existing class diagram
    with open(diagram_filepath, 'r', encoding='utf8') as expected_puml_file:
        assert_py2puml_is_stringio(domain_path, domain_module, expected_puml_file)

def assert_py2puml_is_stringio(domain_path: str, domain_module: str, expected_content_stream: StringIO):
    # generates the PlantUML documentation
    puml_content = list(py2puml(domain_path, domain_module))

    assert_multilines(puml_content, expected_content_stream)


def assert_multilines(actual_multilines: List[str], expected_multilines: Iterable[str]):
    line_index = 0
    for line_index, (actual_line, expected_line) in enumerate(zip(actual_multilines, expected_multilines)):
        assert actual_line == expected_line, f'actual and expected contents have changed at line {line_index + 1}: {actual_line=}, {expected_line=}'
    
    assert line_index + 1 == len(actual_multilines), f'actual and expected diagrams have {line_index + 1} lines'