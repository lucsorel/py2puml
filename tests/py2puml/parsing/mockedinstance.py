class MockedInstance:
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
