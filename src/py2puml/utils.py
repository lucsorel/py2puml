from typing import Type


def investigate_domain_definition(type_to_inspect: Type):
    """
    Utilitary function which inspects the annotations of the given type
    """
    type_annotations = getattr(type_to_inspect, '__annotations__', None)
    if type_annotations is None:
        # print(f'class {type_to_inspect.__module__}.{type_to_inspect.__name__} of type {type(type_to_inspect)} has no annotation')
        for attr_class_key in dir(type_to_inspect):
            if attr_class_key != '__doc__':
                print(f'{type_to_inspect.__name__}.{attr_class_key}:', getattr(type_to_inspect, attr_class_key))
    else:
        # print(type_to_inspect.__annotations__)
        for attr_name, attr_class in type_annotations.items():
            for attr_class_key in dir(attr_class):
                if attr_class_key != '__doc__':
                    print(
                        f'{type_to_inspect.__name__}.{attr_name}:', attr_class_key, getattr(attr_class, attr_class_key)
                    )
