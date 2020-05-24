from typing import Type

def inspect_type(type: Type):
    '''
    Utilitary function which inspects the annotations of the given type
    '''
    type_annotations = getattr(type, '__annotations__', None)
    if type_annotations is None:
        print(f'class {type.__module__}.{type.__name__} has no annotation')
    else:
        # print(type.__annotations__)
        for attr_name, attr_class in type_annotations.items():
            for attr_class_key in dir(attr_class):
                if attr_class_key != '__doc__':
                    print(
                        f'{type.__name__}.{attr_name}:',
                        attr_class_key, getattr(attr_class, attr_class_key)
                    )
