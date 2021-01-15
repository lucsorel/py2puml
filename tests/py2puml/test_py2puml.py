from py2puml import __version__, py2puml


def test_version():
    assert __version__ == '0.3.1'


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
