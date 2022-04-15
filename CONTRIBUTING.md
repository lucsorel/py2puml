
You would like to contribute to `py2puml`, thank you very much!

Here are a few tips and guidelines to help you in the process.

# State of mind

This is an open-source library that I maintain during my free time, which I do not have much:

* I do what I can to give you some feedback (either a direct response or a message about my unavailability)
* everybody does her best while communicating but misunderstanding happens often when discussing asynchronously with textual message; let's speak friendly and welcome reformulation requests the best we can
* English is the language that we shall use to communicate, let's all be aware that English may not be our native language.

# Process

1. check in the issues (in the closed ones too) if the problem you are facing has already been mentionned, contribute to existing and matching issues before creating a new one
1. create a new issue if an existing one does not exist already and let's discuss the new feature you request or the bug you are facing.
Details about the way to reproduce a bug helps to fix it
1. fork the project
1. implement the feature or fix the bug.
Corresponding unit tests must be added or adapted according to what was discussed in the issue
1. create a pull-request and notify the library contributors (see the [Contributions](README.md#contributions) section)

All text files are expected to be encoded in UTF-8.

## Contributions and version update

Add yourself at the bottom of the [contributions section of the README.md](README.md#contributions) file:

```text
# Contributions

* [Luc Sorel-Giffo](https://github.com/lucsorel)
* ...
* [Your Full Name](https://github.com/yourgithubname)
```

Discuss the new version number in the pull request and add a changelog line at the top of the [Changelog section of the README.md](README.md#changelog) file:

```text
# Changelog

* `major.minor.patch`: the feature you added
* ...
```

The version number is carried by the [pyproject.toml](pyproject.toml) file, which is not installed along the production code.
Some manual changes thus need to be made to update it in the CLI; please, update the version number:

- in the [version attribute of the pyproject.toml](pyproject.toml#L3) file

```toml
[tool.poetry]
name = "py2puml"
version = "major.minor.patch"
```

- in the [cli.py module](py2puml/cli.py#L12) (the string value associated to the `version` parameter)
- in the [test__init__.py](tests/py2puml/test__init__.py#L5) file


# Code practices

It takes time to write comprehensive guidelines.
To save time (my writing time and your reading time), I tried to make it short so my best advice is _go have a look at the production and test codes and try to follow the conventions you draw from what you see_ 🙂

## Unit tests

Pull requests must come with unit tests, either new ones (for feature addtitions), changed ones (for feature changes) or non-regression ones (for bug fixes).
Have a look at the [tests](tests/) folder and the existing automated tests scripts to see how they are organized:

* within the `tests` folder, the subfolders' structure follows the one of the `py2puml` production code
* it helps finding the best location to write the unit tests, and where to find the ones corresponding to a feature you want to understand better

This project uses the [pytest](https://docs.pytest.org) framework to run the whole tests suit.
It provides useful features like the parametrization of unit test functions and local mocking for example.

## Code styling

Use pythonesque features (list or dict comprehensions, generators) when possible and relevant.

Use **type annotations** in function signatures and for variables receiving the result of a function call.

When manipulating **literal strings**:

```python
'favor single quote delimiters'
"use double quote delimiters if the text contains some 'single quotes'"
'''use triple quote delimiters if the text contains both "double" and 'single' quote delimiters'''

python_version = '3.8+'
f'use f-strings to format strings, py2puml use Python {python_version}'
```

### Code formatting

#### Imports

The following guidelines regarding imports are designed to help people understand what a Python module does or deals with:

* place import statements at the top of the file
* explicit the functionalities you import with the `from ... import ...` syntax instead of importing a whole module (it does not tell how this module is being used)
* order the imports by family of modules:
  1. the native modules (the types imported from the typing module are often placed first)
  1. the dependency modules defined in the [pyproject.toml file](pyproject.toml) (`py2puml` only use development dependencies)
  1. the modules of the `py2puml` package
* when they are so many items imported from a module that they do not fit on a single line, wrap them with a pair of parentheses instead of using a backslash

```python
from typing import Dict, List, Tuple

from ast import (
    NodeVisitor, arg, expr,
    FunctionDef, Assign, AnnAssign,
    Attribute, Name, Tuple as AstTuple,
    Subscript, get_source_segment
)
from collections import namedtuple

from py2puml.domain.umlclass import UmlAttribute
from py2puml.domain.umlrelation import UmlRelation, RelType
```

#### Code indentation

Most settings in Python-code editors replace tabulation by 4 space characters.
That is what is used for this library as well.

This library follows an opiniated way for formatting the code between **parentheses, brackets or braces**.
Whenever a block of python expressions is surrounded by a pair of parentheses, brackets or braces:

* start the inner content in an indented block (one tabulation is enough) in a new line following the opening parenthesis, bracket or brace
* type the closing parenthesis, bracket or brace in a new line, de-indent so that the inner content is visually enclosed between the opening and closing symbol
* repeat the logic within the inner content block

Some examples:

```python
# function signature and return type
def parse_class_constructor(
    class_type: Type,
    class_fqn: str, root_module_name: str
) -> Tuple[
    List[UmlAttribute], Dict[str, UmlRelation]
]:
    constructor = getattr(class_type, '__init__', None)
    ...

# function call
print(''.join(
    py2puml('py2puml/domain', 'py2puml.domain')
))

# using a generator to get the first matching item
definition_module_member = next((
    member for member in definition_members
    # ensures that the type belongs to the module being parsed
    if member[0] == '__module__' and member[1].startswith(root_module_name)
), None)

# dictionary comprehension with a complex filtering expression
def extend_relations(self, target_fqns: List[str]):
    self.uml_relations_by_target_fqn.update({
        target_fqn: UmlRelation(self.class_fqn, target_fqn, RelType.COMPOSITION)
        for target_fqn in target_fqns
        if target_fqn.startswith(self.root_fqn) and (
            target_fqn not in self.uml_relations_by_target_fqn
        )
    })
```

I am looking forward to providing the linting settings corresponding to these practices.
