from io import StringIO
from typing import Iterable, List

from pytest import mark

from py2puml.asserts import normalize_lines_with_returns

PY2PUML_HEADER = """@startuml py2puml.domain
!pragma useIntermediatePackages false
"""


@mark.parametrize(
    ['input_lines_with_returns', 'expected_lines'],
    [
        (['line'], ['line']),
        (['line\n'], ['line', '']),
        ([PY2PUML_HEADER], ['@startuml py2puml.domain', '!pragma useIntermediatePackages false', '']),
        (StringIO(PY2PUML_HEADER), ['@startuml py2puml.domain', '!pragma useIntermediatePackages false', '']),
    ],
)
def test_normalize_lines_with_returns(input_lines_with_returns: Iterable[str], expected_lines: List[str]):
    assert normalize_lines_with_returns(input_lines_with_returns) == expected_lines
