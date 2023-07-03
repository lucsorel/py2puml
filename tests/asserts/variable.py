from ast import get_source_segment

from py2puml.parsing.astvisitors import Variable


def assert_Variable(variable: Variable, id: str, type_str: str, source_code: str):
    assert variable.id == id
    if type_str is None:
        assert variable.type_expr is None, 'no type annotation'
    else:
        assert get_source_segment(source_code, variable.type_expr) == type_str
