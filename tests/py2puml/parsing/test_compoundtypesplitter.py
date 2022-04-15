from typing import Tuple

from pytest import mark, raises

from py2puml.parsing.compoundtypesplitter import CompoundTypeSplitter, remove_forward_references


@mark.parametrize(
    'type_annotation',
    [
        'int',
        'str',
        '_ast.Name',
        'Tuple[str, withenum.TimeUnit]',
        'List[datetime.date]',
        'modules.withenum.TimeUnit',
        'Dict[str, Dict[str,builtins.float]]',
    ],
)
def test_CompoundTypeSplitter_from_valid_types(type_annotation: str):
    splitter = CompoundTypeSplitter(type_annotation, 'type.module')
    assert splitter.compound_type_annotation == type_annotation


@mark.parametrize(
    'type_annotation',
    [
        None,
        '',
        '@dataclass',
        'Dict[str: withenum.TimeUnit]',
    ],
)
def test_CompoundTypeSplitter_from_invalid_types(type_annotation: str):
    with raises(ValueError) as ve:
        splitter = CompoundTypeSplitter(type_annotation, 'type.module')
    assert str(ve.value) == f'{type_annotation} seems to be an invalid type annotation'


@mark.parametrize(
    'type_annotation,expected_parts',
    [
        ('int', ('int',)),
        ('str', ('str',)),
        ('_ast.Name', ('_ast.Name',)),
        (
            'Tuple[str, withenum.TimeUnit]',
            ('Tuple', '[', 'str', ',', 'withenum.TimeUnit', ']'),
        ),
        ('List[datetime.date]', ('List', '[', 'datetime.date', ']')),
        ('List[IPv6]', ('List', '[', 'IPv6', ']')),
        ('modules.withenum.TimeUnit', ('modules.withenum.TimeUnit',)),
        (
            'Dict[str, Dict[str,builtins.float]]',
            (
                'Dict',
                '[',
                'str',
                ',',
                'Dict',
                '[',
                'str',
                ',',
                'builtins.float',
                ']',
                ']',
            ),
        ),
        ('typing.List[Package]', ('typing.List', '[', 'Package', ']')),
        (
            "typing.List[ForwardRef('Package')]",
            ('typing.List', '[', 'py2puml.domain.package.Package', ']'),
        ),
        (
            'typing.List[py2puml.domain.umlclass.UmlAttribute]',
            ('typing.List', '[', 'py2puml.domain.umlclass.UmlAttribute', ']'),
        ),
    ],
)
def test_CompoundTypeSplitter_get_parts(type_annotation: str, expected_parts: Tuple[str]):
    splitter = CompoundTypeSplitter(type_annotation, 'py2puml.domain.package')
    assert splitter.get_parts() == expected_parts


@mark.parametrize(
    'type_annotation,type_module,without_forward_references',
    [
        (None, None, None),
        (
            "typing.List[ForwardRef('Package')]",
            'py2puml.domain.package',
            'typing.List[py2puml.domain.package.Package]',
        ),
    ],
)
def test_remove_forward_references(type_annotation: str, type_module: str, without_forward_references: str):
    assert remove_forward_references(type_annotation, type_module) == without_forward_references
