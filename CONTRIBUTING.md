
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

To homogenize code style consistency and enforce code quality, this project uses:

- the `ruff` linter and formatter
- the `isort` formatter for imports, because it handles the 'tests' sections in the imports
- `pre-commit` hooks that are triggered on the Github CI (in pull-requests) and should be activated locally when contributing to the project:

```sh
# installs the dependencies, including pre-commit as a lint dependency
poetry install

# activates the pre-commit hooks
poetry run pre-commit install --hook-type pre-commit --hook-type commit-msg

# runs the code quality hooks on the codebase
poetry run pre-commit run --all-files
```

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
