
from py2puml.inspection.moduleresolver import ModuleResolver

class MockedInstance(object):
    '''
    Creates an object instance from a dictionary
    so that access paths like dict['key1']['key2']['key3'] can be replaced by instance.key1.key2.key3
    '''
    def __init__(self, inner_attributes_as_dict: dict):
        self.update_instance_dict(self, inner_attributes_as_dict)

    def update_instance_dict(self, instance, attributes_dict: dict):
        instance.__dict__.update(attributes_dict)
        for instance_attribute, value in attributes_dict.items():
            if isinstance(value, dict):
                setattr(instance, instance_attribute, MockedInstance(value))


def test_ModuleResolver_resolve_full_namespace_type():
    source_module = MockedInstance({
        '__name__': 'tests.modules.withconstructor',
        'modules': {
            'withenum': {
                'TimeUnit': {
                    '__module__': 'tests.modules.withenum',
                    '__name__': 'TimeUnit'
                }
            }
        },
        'withenum': {
            'TimeUnit': {
                '__module__': 'tests.modules.withenum',
                '__name__': 'TimeUnit'
            }
        },
        'Coordinates': {
            '__module__': 'tests.modules.withconstructor',
            '__name__': 'Coordinates'
        }
    })
    module_resolver = ModuleResolver(source_module)
    assert module_resolver.resolve_full_namespace_type(
        'modules.withenum.TimeUnit'
    ) == 'tests.modules.withenum.TimeUnit'
    assert module_resolver.resolve_full_namespace_type(
        'withenum.TimeUnit'
    ) == 'tests.modules.withenum.TimeUnit'
    assert module_resolver.resolve_full_namespace_type(
        'Coordinates'
    ) == 'tests.modules.withconstructor.Coordinates'

def test_ModuleResolver_get_module_full_name():
    source_module = MockedInstance({
        '__name__': 'tests.modules.withconstructor'
    })
    module_resolver = ModuleResolver(source_module)
    assert module_resolver.get_module_full_name() == 'tests.modules.withconstructor'
