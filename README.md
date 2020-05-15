Generate Plantuml diagrams to document your python code

# How it works

From a given path corresponding to a folder containing python code, `py2puml` loads each file as a module and generate a class diagram with the [PlantUML](https://plantuml.com/en/class-diagram) using:

* inspection to detect the classes to document (see the [inspect](https://docs.python.org/3/library/inspect.html) module)
* annotations (the python type hinting syntax) to detect the attributes and their types (see the [typing](https://docs.python.org/3/library/typing.html) module)

Current limitations:

* type hinting is optional when writing the code and discarded when it is executed, as mentionned in the official documentation. The quality of the diagram output by `py2puml` depends on the reliability with which the annotations were written

> The Python runtime does not enforce function and variable type annotations. They can be used by third party tools such as type checkers, IDEs, linters, etc.

* complex type hints with more than one level of genericity are not properly handled for the moment: `List[MyClass]` or `Dict[str, MyClass]` are handled properly, `Dict[str, List[MyClass]]` is not. If your domain classes (also called business objects or DTOs) have attributes with complex type hints, it may be a code smell indicating that you should write a class which would better represent the business logic. But I may improve this part of the library as well 😀

* composition relationships are detected and drawn. Inheritance relationships are not handled for now

* `py2puml` does not inspect sub-folders recursively, but it is planned

* `py2puml` outputs diagrams in PlantUML syntax, which can be saved in text files along your python code and versioned with them. To generate image files, use the PlantUML runtime or a docker image (see [think/plantuml](https://hub.docker.com/r/think/plantuml))

* `py2puml` uses features of python 3 (generators for example) and thus won't work with python 2 runtimes. It relies on native python modules and uses no 3rd-party library, except [pytest](https://docs.pytest.org/en/latest/) as a development dependency for running the unit-tests

You may also be interested in this [lucsorel/plantuml-file-loader](https://github.com/lucsorel/plantuml-file-loader) project: A webpack loader which converts PlantUML files into images during the webpack processing (useful to [include PlantUML diagrams in your slides](https://github.com/lucsorel/markdown-image-loader/blob/master/README.md#web-based-slideshows) with RevealJS or RemarkJS).

# Install

Install from the github repository:

* with `pip`:

```sh
pip3 install git+https://github.com/lucsorel/py2puml.git
```

* with [poetry](https://pipenv.readthedocs.io/en/latest/):

```sh
poetry add git+https://github.com/lucsorel/py2puml.git
```

* with [pipenv](https://pipenv.readthedocs.io/en/latest/):

```sh
# should be installed in editable mode to ensure an up-to-date copy of the repository and that it includes all known dependencies -> '-e'
pipenv install -e git+https://github.com/lucsorel/py2puml.git#egg=py2puml
```

# Usage

For example, to create the diagram of the classes used by `py2puml`:

* import the py2puml function in your script (see [py2puml/example.py](py2puml/example.py)):

```python
from py2puml.py2puml import py2puml

# outputs the PlantUML content in the terminal
print(''.join(py2puml('py2puml/domain', 'py2puml.domain')))

# writes the PlantUML content in a file
with open('py2puml/domain.puml', 'w') as puml_file:
    puml_file.writelines(py2puml('py2puml/domain', 'py2puml.domain'))
```

* running it (`python3 -m py2puml.example`) will output the PlantUML diagram in the terminal and write it in a file

```plantuml
@startuml
class py2puml.domain.umlattribute.UmlAttribute {
  name: str
  type: str
}
class py2puml.domain.umlclass.UmlClass {
  name: str
  fqdn: str
  attributes: List[UmlAttribute]
}
class py2puml.domain.umlcomposition.UmlComposition {
  compound_fqdn: str
  component_fqdn: str
}
py2puml.domain.umlclass.UmlClass *-- py2puml.domain.umlattribute.UmlAttribute
@enduml
```

Which renders like this:

![](https://www.plantuml.com/plantuml/png/ZP0_2y8m4CNtV8gRXNPmx5HnTNKIaMWY199Bp5s68ltkfi7KWlXd-xrty7uXFR6Cd9mL5ok980pha5Ehl9C6suoIEPfpOjtkdTtK07S1WDBf3eXZPXx2ayUFKwMVPhOJl4rSRmehprRgO6U83qlvyPl3k-39iF5OJAzOVEMSK9rcMIrH8o_QKVny_wff_lulqMjK-Ve0)

# Tests

```sh
poetry run python3 -W ignore::DeprecationWarning -m pytest -v
```

# Licence

Unless stated otherwise all works are licensed under the [MIT license](http://spdx.org/licenses/MIT.html), a copy of which is included [here](LICENSE).

# Contributions

* [Luc Sorel-Giffo](https://github.com/lucsorel)

Pull-requests are welcome and will be processed on a best-effort basis.


# Alternatives

If `py2uml` does not meet your needs (suggestions and pull-requests are welcome), you can have a look at these projects which follow other approaches (AST, linting, modeling):

* [cb109/pyplantuml](https://github.com/cb109/pyplantuml)
* [deadbok/py-puml-tools](https://github.com/deadbok/py-puml-tools)
* [caballero/genUML](https://github.com/jose-caballero/genUML)
