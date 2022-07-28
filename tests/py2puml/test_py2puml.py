
from pathlib import Path

from py2puml.py2puml import py2puml


CURRENT_DIR = Path(__file__).parent

def test_py2puml_model_on_py2uml_domain():
    domain_diagram_file_path = CURRENT_DIR.parent.parent / 'py2puml' / 'py2puml.domain.puml'

    # generates the PlantUML documentation
    puml_content = list(py2puml('py2puml/domain', 'py2puml.domain'))

    # reads the existing class diagram (update it with `python -m py2puml.example`)
    with open(domain_diagram_file_path, 'r', encoding='utf8') as expected_puml_file:
        line_index = 0
        for line_index, (actual_line, expected_line) in enumerate(zip(puml_content, expected_puml_file)):
            assert actual_line == expected_line, f'updated and versionned content {domain_diagram_file_path} in line {line_index} has changed'
        
        assert line_index + 1 == len(puml_content), f'actual and expected diagrams have {line_index + 1} lines'


def test_py2puml_with_subdomain():
    expected = """@startuml tests.modules.withsubdomain
namespace tests.modules.withsubdomain {
  namespace subdomain.insubdomain {}
  namespace withsubdomain {}
}
class tests.modules.withsubdomain.subdomain.insubdomain.Engine {
  horsepower: int
}
class tests.modules.withsubdomain.subdomain.insubdomain.Pilot {
  name: str
}
class tests.modules.withsubdomain.withsubdomain.Car {
  name: str
  engine: Engine
}
tests.modules.withsubdomain.withsubdomain.Car *-- tests.modules.withsubdomain.subdomain.insubdomain.Engine
@enduml
"""
    puml_content = py2puml(
      'tests/modules/withsubdomain/', 'tests.modules.withsubdomain'
    )
    assert ''.join(puml_content) == expected
