from functools import wraps


def count_signature_args(func):
    @wraps(func)
    def signature_args_counter(*args, **kwargs):
        print(f'{len(args)} positional arguments, {len(kwargs)} keyword arguments')

        func(*args, **kwargs)

    return signature_args_counter


def signature_arg_values(func):
    @wraps(func)
    def signature_values_lister(*args, **kwargs):
        print('positional arguments:', ', '.join(str(arg) for arg in args))
        print('keyword arguments:', ', '.join(f'{key}: {value}' for key, value in kwargs.items()))
        func(*args, **kwargs)

    return signature_values_lister


class Point:
    """
    A Point class, with a constructor which is decorated by wrapping decorators
    """

    @count_signature_args
    @signature_arg_values
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


# Point(2.5, y=3.2)


def signature_improper_decorator(func):
    def not_wrapping_decorator(*args, **kwargs):
        print(f'{len(args) + len(kwargs)} arguments')
        func(*args, **kwargs)

    return not_wrapping_decorator


class PointDecoratedWithoutWrapping:
    """
    A Point class, with a constructor which is decorated by wrapping decorators
    """

    @signature_improper_decorator
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


# PointDecoratedWithoutWrapping(2.5, y=3.2)
