from io import StringIO
from pathlib import Path
from typing import Union

from py2puml.py2puml import py2puml


def assert_py2puml_is_file_content(domain_path: str, domain_module: str, diagram_filepath: Union[str, Path]):
    # reads the existing class diagram
    with open(diagram_filepath, 'r', encoding='utf8') as expected_puml_file:
        assert_py2puml_is_stringio(domain_path, domain_module, expected_puml_file)

def assert_py2puml_is_stringio(domain_path: str, domain_module: str, expected_content_stream: StringIO):
    # generates the PlantUML documentation
    puml_content = list(py2puml(domain_path, domain_module))
    line_index = 0
    for line_index, (actual_line, expected_line) in enumerate(zip(puml_content, expected_content_stream)):
        assert actual_line == expected_line, f'updated and versionned content {domain_diagram_file_path} in line {line_index} has changed'
    
    assert line_index + 1 == len(puml_content), f'actual and expected diagrams have {line_index + 1} lines'
