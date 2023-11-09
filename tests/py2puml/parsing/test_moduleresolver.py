from py2puml.parsing.moduleresolver import ModuleResolver, NamespacedType

from tests.py2puml.parsing.mockedinstance import MockedInstance


def assert_NamespacedType(namespaced_type: NamespacedType, full_namespace_type: str, short_type: str):
    assert namespaced_type.full_namespace == full_namespace_type
    assert namespaced_type.type_name == short_type


def test_ModuleResolver_resolve_full_namespace_type():
    source_module = MockedInstance(
        {
            '__name__': 'tests.modules.withconstructor',
            'modules': {'withenum': {'TimeUnit': {'__module__': 'tests.modules.withenum', '__name__': 'TimeUnit'}}},
            'withenum': {'TimeUnit': {'__module__': 'tests.modules.withenum', '__name__': 'TimeUnit'}},
            'Coordinates': {'__module__': 'tests.modules.withconstructor', '__name__': 'Coordinates'},
        }
    )
    module_resolver = ModuleResolver(source_module)
    assert_NamespacedType(
        module_resolver.resolve_full_namespace_type('modules.withenum.TimeUnit'),
        'tests.modules.withenum.TimeUnit',
        'TimeUnit',
    )
    assert_NamespacedType(
        module_resolver.resolve_full_namespace_type('withenum.TimeUnit'), 'tests.modules.withenum.TimeUnit', 'TimeUnit'
    )
    assert_NamespacedType(
        module_resolver.resolve_full_namespace_type('Coordinates'),
        'tests.modules.withconstructor.Coordinates',
        'Coordinates',
    )


def test_ModuleResolver_get_module_full_name():
    source_module = MockedInstance({'__name__': 'tests.modules.withconstructor'})
    module_resolver = ModuleResolver(source_module)
    assert module_resolver.get_module_full_name() == 'tests.modules.withconstructor'


def test_ModuleResolver_repr():
    source_module = MockedInstance({'__name__': 'tests.modules.withconstructor'})
    module_resolver = ModuleResolver(source_module)
    assert module_resolver.__repr__() == 'ModuleResolver({"__name__": "tests.modules.withconstructor"})'
