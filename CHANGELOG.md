# CHANGELOG

<!-- version list -->

## v0.10.0 (2025-03-27)

### Documentation

- Add Mieszko to contributors, bump version to 0.10.0
  ([`cad916a`](https://github.com/lucsorel/py2puml/commit/cad916a49758fbbed2771b7c9c2a45966c3de6fb))

- **readme**: Add contributors to py2puml ([#143](https://github.com/lucsorel/py2puml/pull/143),
  [`8cf18c0`](https://github.com/lucsorel/py2puml/commit/8cf18c0bd89ae23a0c36ab324a79225700668b4d))


## v0.9.1 (2024-01-30)

### Bug Fixes

- **cli**: Insert the current working directory at the beginning of the PYTHON_PATH to ease module
  resolution ([#82](https://github.com/lucsorel/py2puml/pull/82),
  [`b3f600c`](https://github.com/lucsorel/py2puml/commit/b3f600cb16faa110166be2aa22cb41727f994bdb))

### Documentation

- **readme**: Fix url to PlantUML logo
  ([`673fb11`](https://github.com/lucsorel/py2puml/commit/673fb11be90bf30da548cf55381fa8f8555a12db))


## v0.9.0 (2023-12-30)

### Documentation

- **version**: Set version to 0.9.0, parsing root module is a new feature
  ([#76](https://github.com/lucsorel/py2puml/pull/76),
  [`65a1804`](https://github.com/lucsorel/py2puml/commit/65a180437f3ec86b2105acc124f74470c5e85fa6))

### Features

- Parse __init__.py files in packages. Closes: #52
  ([#76](https://github.com/lucsorel/py2puml/pull/76),
  [`65a1804`](https://github.com/lucsorel/py2puml/commit/65a180437f3ec86b2105acc124f74470c5e85fa6))

- Parse __init__.py files in packages. Closes: #52
  ([#76](https://github.com/lucsorel/py2puml/pull/76),
  [`b1c6c8b`](https://github.com/lucsorel/py2puml/commit/b1c6c8b8491c80fc06c5af08c8a614fddfbe437d))


## v0.8.1 (2023-10-15)

- delegated the grouping of nested namespaces (see `0.7.0`) to the PlantUML binary, which handles it natively

## v0.8.0 (2023-08-28)

### Bug Fixes

- **cli**: Add current working directory to path so that py2puml can import and inspect modules in
  specific folders ([#40](https://github.com/lucsorel/py2puml/pull/40),
  [`175997a`](https://github.com/lucsorel/py2puml/commit/175997a6b63b24e05689684305ae450b911eb023))

- **cli**: Add current working directory to system path so that its modules can be imported and
  inspected by poetry ([#40](https://github.com/lucsorel/py2puml/pull/40),
  [`175997a`](https://github.com/lucsorel/py2puml/commit/175997a6b63b24e05689684305ae450b911eb023))

### Build System

- Improve code coverage (added tests, removed irrelevant code)
  ([#51](https://github.com/lucsorel/py2puml/pull/51),
  [`e9f3c0c`](https://github.com/lucsorel/py2puml/commit/e9f3c0c3d27aeedc1ee76c39b399f641a5a2f24c))

- Remove obsolete init.sh file ([#51](https://github.com/lucsorel/py2puml/pull/51),
  [`e9f3c0c`](https://github.com/lucsorel/py2puml/commit/e9f3c0c3d27aeedc1ee76c39b399f641a5a2f24c))

### Documentation

- **contributing**: Add how to activate the pre-commit hooks
  ([#51](https://github.com/lucsorel/py2puml/pull/51),
  [`e9f3c0c`](https://github.com/lucsorel/py2puml/commit/e9f3c0c3d27aeedc1ee76c39b399f641a5a2f24c))

- **readme**: Add a section about the Python versions required by py2puml and pyenv
  ([#51](https://github.com/lucsorel/py2puml/pull/51),
  [`e9f3c0c`](https://github.com/lucsorel/py2puml/commit/e9f3c0c3d27aeedc1ee76c39b399f641a5a2f24c))

- **readme**: Fix copy-pasted reference to pydoctrace
  ([#51](https://github.com/lucsorel/py2puml/pull/51),
  [`e9f3c0c`](https://github.com/lucsorel/py2puml/commit/e9f3c0c3d27aeedc1ee76c39b399f641a5a2f24c))

### Features

- Handle union type and add pre-commit lint hooks
  ([#51](https://github.com/lucsorel/py2puml/pull/51),
  [`e9f3c0c`](https://github.com/lucsorel/py2puml/commit/e9f3c0c3d27aeedc1ee76c39b399f641a5a2f24c))

- **inspect**: Handle unions in type annotations
  ([#51](https://github.com/lucsorel/py2puml/pull/51),
  [`e9f3c0c`](https://github.com/lucsorel/py2puml/commit/e9f3c0c3d27aeedc1ee76c39b399f641a5a2f24c))


## v0.7.1 (2023-02-12)

### Documentation

- **readme**: Complex compound types are properly handled
  ([#38](https://github.com/lucsorel/py2puml/pull/38),
  [`faa3de0`](https://github.com/lucsorel/py2puml/commit/faa3de0a97d9d6ab97020c03db5d2a04721e1646))

- **readme**: Complex compound types are properly handled
  ([#38](https://github.com/lucsorel/py2puml/pull/38),
  [`5e405cf`](https://github.com/lucsorel/py2puml/commit/5e405cf21e258b5f40bbfa6f493cc6be16ba07ad))


## v0.7.0 (2023-02-12)

### Bug Fixes

- **tests**: Remove undeclared variable, remove unused import
  ([`db134ca`](https://github.com/lucsorel/py2puml/commit/db134ca4bed8704f8fe7e10d7bee65799dc709f3))

### Documentation

- Comments about module resolver
  ([`db134ca`](https://github.com/lucsorel/py2puml/commit/db134ca4bed8704f8fe7e10d7bee65799dc709f3))

- **readme**: Homogenize code formatting
  ([`db134ca`](https://github.com/lucsorel/py2puml/commit/db134ca4bed8704f8fe7e10d7bee65799dc709f3))

- **readme**: Update the PlantUML diagram of the py2puml domain model
  ([`db134ca`](https://github.com/lucsorel/py2puml/commit/db134ca4bed8704f8fe7e10d7bee65799dc709f3))


## v0.6.1 (2023-01-12)

- adoption of conventional commits messages

### Bug Fixes

- **compoundtypesplitter**: Handle class names with digits
  ([#36](https://github.com/lucsorel/py2puml/pull/36),
  [`d708fac`](https://github.com/lucsorel/py2puml/commit/d708facb104a8beaec775423e467487a2947c908))

### Documentation

- **readme**: Fixed version of previous change ([#36](https://github.com/lucsorel/py2puml/pull/36),
  [`d708fac`](https://github.com/lucsorel/py2puml/commit/d708facb104a8beaec775423e467487a2947c908))


## v0.6.0 (2022-04-15)

- handle abstract classes

## v0.5.4 (2021-12-31)

- fixed the packaging so that the contribution guide is included in the published package

## v0.5.3 (2021-12-31)

- handle constructors decorated by wrapping decorators (decorators making uses of `functools.wrap`)

## v0.5.2 (2021-10-04)

- specify in `pyproject.toml` that `py2puml` requires python 3.8+ (`ast.get_source_segment` was introduced in 3.8)

## v0.5.1 (2021-09-09)

- prevent from parsing inherited constructors
- handle instance attributes in class constructors, add code coverage of unit tests (untagged 0.5.1)

## v0.4.0 (2021-03-03)

- add a simple CLI

## v0.3.1 (2021-01-27)

- inspect sub-folders recursively

## v0.3.0 (2020-06-10)

- handle classes derived from namedtuples (attribute types are `Any`)

## v0.2.0 (2020-05-31)
- handle inheritance relationships and enums

## v0.1.3 (2020-05-15)

- first tagged release: handle all modules of a folder and compositions of domain classes

## v0.1.1 (2020-05-15)

- initial release
