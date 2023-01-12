from typing import Tuple

from py2puml.parsing.compoundtypesplitter import CompoundTypeSplitter

from pytest import raises, mark

@mark.parametrize('type_annotation', [
    'int',
    'str',
    '_ast.Name',
    'Tuple[str, withenum.TimeUnit]',
    'List[datetime.date]',
    'modules.withenum.TimeUnit',
    'Dict[str, Dict[str,builtins.float]]',
])
def test_CompoundTypeSplitter_from_valid_types(type_annotation: str):
    splitter = CompoundTypeSplitter(type_annotation)
    assert splitter.compound_type_annotation == type_annotation

@mark.parametrize('type_annotation', [
    None,
    '',
    '@dataclass',
    'Dict[str: withenum.TimeUnit]',
])
def test_CompoundTypeSplitter_from_invalid_types(type_annotation: str):
    with raises(ValueError) as ve:
        splitter = CompoundTypeSplitter(type_annotation)
    assert str(ve.value) == f'{type_annotation} seems to be an invalid type annotation'

@mark.parametrize('type_annotation,expected_parts', [
    ('int', ('int',)),
    ('str', ('str',)),
    ('_ast.Name', ('_ast.Name',)),
    ('Tuple[str, withenum.TimeUnit]', ('Tuple', '[', 'str', ',', 'withenum.TimeUnit', ']')),
    ('List[datetime.date]', ('List', '[', 'datetime.date', ']')),
    ('List[IPv6]', ('List', '[', 'IPv6', ']')),
    ('modules.withenum.TimeUnit', ('modules.withenum.TimeUnit',)),
    ('Dict[str, Dict[str,builtins.float]]', ('Dict', '[', 'str', ',', 'Dict', '[', 'str', ',', 'builtins.float', ']', ']')),
])
def test_CompoundTypeSplitter_get_parts(type_annotation: str, expected_parts: Tuple[str]):
    splitter = CompoundTypeSplitter(type_annotation)
    assert splitter.get_parts() == expected_parts
