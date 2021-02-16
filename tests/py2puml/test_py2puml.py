from subprocess import run, PIPE

from py2puml import __version__, __description__, py2puml


def test_version():
    assert __version__ == '0.4.0'

def test_description():
    assert __description__ == 'Generate Plantuml diagrams to document your python code'


def test_py2puml_model():
    """test py2puml on py2puml/domain."""
    expected = """@startuml
class py2puml.domain.umlclass.UmlAttribute {
  name: str
  type: str
}
class py2puml.domain.umlclass.UmlClass {
  attributes: List[UmlAttribute]
}
class py2puml.domain.umlitem.UmlItem {
  name: str
  fqdn: str
}
class py2puml.domain.umlenum.Member {
  name: str
  value: str
}
class py2puml.domain.umlenum.UmlEnum {
  members: List[Member]
}
enum py2puml.domain.umlrelation.RelType {
  COMPOSITION: *
  INHERITANCE: <|
}
class py2puml.domain.umlrelation.UmlRelation {
  source_fqdn: str
  target_fqdn: str
  type: RelType
}
py2puml.domain.umlclass.UmlClass *-- py2puml.domain.umlclass.UmlAttribute
py2puml.domain.umlitem.UmlItem <|-- py2puml.domain.umlclass.UmlClass
py2puml.domain.umlenum.UmlEnum *-- py2puml.domain.umlenum.Member
py2puml.domain.umlitem.UmlItem <|-- py2puml.domain.umlenum.UmlEnum
py2puml.domain.umlrelation.UmlRelation *-- py2puml.domain.umlrelation.RelType
@enduml
"""
    puml_content = py2puml.py2puml('py2puml/domain', 'py2puml.domain')
    assert ''.join(puml_content) == expected


def test_py2puml_with_subdomain():
    expected = """@startuml
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
    puml_content = py2puml.py2puml(
      'tests/modules/withsubdomain/', 'tests.modules.withsubdomain'
    )
    assert ''.join(puml_content) == expected


def test_cli_consistency():
    """ Check CLI consistency with the default configuration."""
    cli_stdout = run(
        ['py2puml', 'py2puml/domain', 'py2puml.domain'],
        stdout=PIPE, stderr=PIPE,
        text=True, check=True
    ).stdout

    puml_content = py2puml.py2puml('py2puml/domain', 'py2puml.domain')

    assert ''.join(puml_content).strip() == cli_stdout.strip()

def test_cli_module_consistency():
    """ Check CLI-as-a-module consistency with the default configuration."""
    cli_stdout = run(
        ['python', '-m', 'py2puml.cli', 'py2puml/domain', 'py2puml.domain'],
        stdout=PIPE, stderr=PIPE,
        text=True, check=True
    ).stdout

    puml_content = py2puml.py2puml('py2puml/domain', 'py2puml.domain')

    assert ''.join(puml_content).strip() == cli_stdout.strip()
