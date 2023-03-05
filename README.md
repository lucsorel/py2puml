<div align="center">
  <a href="https://www.python.org/psf-landing/" target="_blank">
    <img width="350px" alt="Python logo"
      src="https://www.python.org/static/community_logos/python-logo-generic.svg" />
  </a>
  <a href="http://plantuml.com/" target="_blank">
    <img width="116px" height="112px" alt="PlantUML logo" src="http://s.plantuml.com/logoc.png" style="margin-bottom: 40px" vspace="40px" />
  </a>
  <h1>Python to PlantUML</h1>
</div>

Generate PlantUML class diagrams to document your Python application.

# How it works

`py2puml` produces a class diagram [PlantUML script](https://plantuml.com/en/class-diagram) representing classes properties (static and instance attributes) and their relations (composition and inheritance relationships).

`py2puml` internally uses code [inspection](https://docs.python.org/3/library/inspect.html) (also called *reflexion* in other programming languages) and [abstract tree parsing](https://docs.python.org/3/library/ast.html) to retrieve relevant information.
Some parsing features are available only since Python 3.8 (like [ast.get_source_segment](https://docs.python.org/3/library/ast.html#ast.get_source_segment)).

## Features

From a given path corresponding to a folder containing Python code, `py2puml` processes each Python module and generates a [PlantUML script](https://plantuml.com/en/class-diagram) from the definitions of various data structures using:

* **[inspection](https://docs.python.org/3/library/inspect.html)** and [type annotations](https://docs.python.org/3/library/typing.html) to detect:
  * static class attributes and [dataclass](https://docs.python.org/3/library/dataclasses.html) fields
  * fields of [namedtuples](https://docs.python.org/3/library/collections.html#collections.namedtuple)
  * members of [enumerations](https://docs.python.org/3/library/enum.html)
  * composition and inheritance relationships (between your domain classes only, for documentation sake).
The detection of composition relationships relies on type annotations only, assigned values or expressions are never evaluated to prevent unwanted side-effects

* parsing **[abstract syntax trees](https://docs.python.org/3/library/ast.html#ast.NodeVisitor)** to detect the instance attributes defined in `__init__` constructors

`py2puml` outputs diagrams in PlantUML syntax, which can be:
* versioned along your code with a unit-test ensuring its consistency (see the [test_py2puml.py's test_py2puml_model_on_py2uml_domain](tests/py2puml/test_py2puml.py) example)
* generated and hosted along other code documentation (better option: generated documentation should not be versioned with the codebase)

To generate image files, use the PlantUML runtime, a docker image of the runtime (see [think/plantuml](https://hub.docker.com/r/think/plantuml)) or of a server (see the CLI documentation below)

If you like tools related with PlantUML, you may also be interested in this [lucsorel/plantuml-file-loader](https://github.com/lucsorel/plantuml-file-loader) project:
a webpack loader which converts PlantUML files into images during the webpack processing (useful to [include PlantUML diagrams in your slides](https://github.com/lucsorel/markdown-image-loader/blob/master/README.md#web-based-slideshows) with RevealJS or RemarkJS).

# Install

Install from [PyPI](https://pypi.org/project/py2puml/):

* with `pip`:

```sh
pip install py2puml
```

* with [poetry](https://python-poetry.org/docs/):

```sh
poetry add py2puml
```

* with [pipenv](https://pipenv.readthedocs.io/en/latest/):

```sh
pipenv install py2puml
```

# Usage

## CLI

Once `py2puml` is installed at the system level, an eponymous command is available in your environment shell.

For example, to create the diagram of the classes used by `py2puml`, run:

```sh
py2puml py2puml/domain py2puml.domain
```

This outputs the following PlantUML content:

```plantuml
@startuml py2puml.domain
namespace py2puml.domain {
  namespace package {}
  namespace umlclass {}
  namespace umlitem {}
  namespace umlenum {}
  namespace umlrelation {}
}
class py2puml.domain.package.Package {
  name: str
  children: List[Package]
  items_number: int
}
class py2puml.domain.umlclass.UmlAttribute {
  name: str
  type: str
  static: bool
}
class py2puml.domain.umlclass.UmlClass {
  attributes: List[UmlAttribute]
  is_abstract: bool
}
class py2puml.domain.umlitem.UmlItem {
  name: str
  fqn: str
}
class py2puml.domain.umlenum.Member {
  name: str
  value: str
}
class py2puml.domain.umlenum.UmlEnum {
  members: List[Member]
}
enum py2puml.domain.umlrelation.RelType {
  COMPOSITION: * {static}
  INHERITANCE: <| {static}
}
class py2puml.domain.umlrelation.UmlRelation {
  source_fqn: str
  target_fqn: str
  type: RelType
}
py2puml.domain.package.Package *-- py2puml.domain.package.Package
py2puml.domain.umlclass.UmlClass *-- py2puml.domain.umlclass.UmlAttribute
py2puml.domain.umlitem.UmlItem <|-- py2puml.domain.umlclass.UmlClass
py2puml.domain.umlenum.UmlEnum *-- py2puml.domain.umlenum.Member
py2puml.domain.umlitem.UmlItem <|-- py2puml.domain.umlenum.UmlEnum
py2puml.domain.umlrelation.UmlRelation *-- py2puml.domain.umlrelation.RelType
footer Generated by //py2puml//
@enduml
```

Using PlantUML, this content is rendered as this diagram:

![py2puml domain UML Diagram](https://www.plantuml.com/plantuml/png/ZPD1Yzim48Nl-XLpNbWRUZHxs2M4rj1DbZGzbIN8zcmgAikkD2wO9F-zigqWEw1L3i6HPgJlFUdfsH3NrDKIslvBQxz9rTHSAAPuZQRb9TuKuCG0PaLU_k5776S1IicDkLcGk9RaRT4wRPA18Ut6vMyXAuqgW-_2q2_N_kwgWh0s1zNL1UeCXA9n_iAcdnTamQEApnHTUvAVjNmXqgBeAAoB-dOnDiH9b1aKJIETYBj8gvai07xb6kTtfiMRDWTUM38loV62feVpYNWUMWOXkVq6tNxyLMuO8g7g8gIn9Nd5uQw2e7zSTZX7HJUqqjUU3L2FWElvJRZti6wDafDeb5i_shWb-QvaXtBVjpuMg-ths_P7li-tcmmUu3J5uEAg-URRUfVlNpQhTGPFPr-EUlD4ws-tr0XWcawNU5ZS2W1nVKJoi_EWEjspSxYmo8jyU7oCF5eMoxNV8_BCM2INJsUxKOp68WdnOWAfl5j56CBkl4cd9H8pzj4qX1g-eaBD2IieUaXJjp1DsJEgolvZ_m40)

For a full overview of the CLI, run:

```sh
py2puml --help
```

The CLI can also be launched as a python module:

```sh
python -m py2puml py2puml/domain py2puml.domain
```

Pipe the result of the CLI with a PlantUML server for instantaneous documentation (rendered by ImageMagick):

```sh
# runs a local PlantUML server from a docker container:
docker run -d --rm -p 1234:8080 --name plantumlserver plantuml/plantuml-server:jetty

py2puml py2puml/domain py2puml.domain | curl -X POST --data-binary @- http://localhost:1234/svg/ --output - | display

# stops the container when you don't need it anymore, restarts it later
docker stop plantumlserver
docker start plantumlserver
```

## Python API

For example, to create the diagram of the classes used by `py2puml`:

* import the `py2puml` function in your script (see [py2puml/example.py](py2puml/example.py)):

```python
from py2puml.py2puml import py2puml

if __name__ == '__main__':
    # outputs the PlantUML content in the terminal
    print(''.join(py2puml('py2puml/domain', 'py2puml.domain')))

    # writes the PlantUML content in a file
    with open('py2puml/domain.puml', 'w') as puml_file:
        puml_file.writelines(py2puml('py2puml/domain', 'py2puml.domain'))
```

* running it (`python3 -m py2puml.example`) outputs the previous PlantUML diagram in the terminal and writes it in a file.


# Tests

```sh
# directly with poetry
poetry run pytest -v

# in a virtual environment
python3 -m pytest -v
```

Code coverage (with [missed branch statements](https://pytest-cov.readthedocs.io/en/latest/config.html?highlight=--cov-branch)):

```sh
poetry run pytest -v --cov=py2puml --cov-branch --cov-report term-missing --cov-fail-under 92
```

# Changelog

* `0.7.2`: added the current working directory to the import path to make py2puml work in any directory or in native virtual environment (not handled by poetry)
* `0.7.1`: removed obsolete part of documentation: deeply compound types are now well handled (by version `0.7.0`)
* `0.7.0`: improved the generated PlantUML documentation (added the namespace structure of the code base, homogenized type  between inspection and parsing), improved relationships management (handle forward references, deduplicate relationships)
* `0.6.1`: handle class names with digits
* `0.6.0`: handle abstract classes
* `0.5.4`: fixed the packaging so that the contribution guide is included in the published package
* `0.5.3`: handle constructors decorated by wrapping decorators (decorators making uses of `functools.wrap`)
* `0.5.2`: specify in pyproject.toml that py2puml requires python 3.8+ (`ast.get_source_segment` was introduced in 3.8)
* `0.5.1`: prevent from parsing inherited constructors
* `0.5.0`: handle instance attributes in class constructors, add code coverage of unit tests
* `0.4.0`: add a simple CLI
* `0.3.1`: inspect sub-folders recursively
* `0.3.0`: handle classes derived from namedtuples (attribute types are `Any`)
* `0.2.0`: handle inheritance relationships and enums
* `0.1.3`: first release, handle all modules of a folder and compositions of domain classes

# Licence

Unless stated otherwise all works are licensed under the [MIT license](http://spdx.org/licenses/MIT.html), a copy of which is included [here](LICENSE).

# Contributions

* [Luc Sorel-Giffo](https://github.com/lucsorel)
* [Doyou Jung](https://github.com/doyou89)
* [Julien Jerphanion](https://github.com/jjerphan)
* [Luis Fernando Villanueva Pérez](https://github.com/jonykalavera)

Pull-requests are welcome and will be processed on a best-effort basis.
Follow the [contributing guide](CONTRIBUTING.md).

# Current limitations

* regarding **inspection**

  * type hinting is optional when writing Python code and discarded when it is executed, as mentionned in the [typing official documentation](https://docs.python.org/3/library/typing.html). The quality of the diagram output by `py2puml` depends on the reliability with which the type annotations were written

  > The Python runtime does not enforce function and variable type annotations. They can be used by third party tools such as type checkers, IDEs, linters, etc.

* regarding the detection of instance attributes with **AST parsing**:
  * only constructors are visited, attributes assigned in other functions won't be documented
  * attribute types are inferred from type annotations:
    * of the attribute itself
    * of the variable assigned to the attribute: a signature parameter or a locale variable
    * to avoid side-effects, no code is executed nor interpreted

# Alternatives

If `py2puml` does not meet your needs (suggestions and pull-requests are **welcome**), you can have a look at these projects which follow other approaches (AST, linting, modeling):

* [pyreverse](https://pylint.pycqa.org/en/latest/additional_commands/index.html#pyreverse), which includes a PlantUML printer [since version 2.10.0](https://pylint.pycqa.org/en/latest/whatsnew/changelog.html?highlight=plantuml#what-s-new-in-pylint-2-10-0)
* [cb109/pyplantuml](https://github.com/cb109/pyplantuml)
* [deadbok/py-puml-tools](https://github.com/deadbok/py-puml-tools)
* [caballero/genUML](https://github.com/jose-caballero/genUML)
