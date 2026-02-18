from itertools import takewhile
from pathlib import Path
from re import compile as re_compile

__description__ = None

PROJECT_PATH = Path(__file__).parent.parent
PROJECT_SRC_PATH = PROJECT_PATH / 'src'
TEST_MODULES_PATH = PROJECT_PATH / 'tests' / 'modules'
DESCRIPTION_PATTERN = re_compile('^description = "([^"]+)"$')


def get_from_line_and_pattern(content_line: str, pattern) -> str:
    pattern_match = pattern.search(content_line)
    if pattern_match is None:
        return None
    else:
        return pattern_match.group(1)


with open(PROJECT_PATH / 'pyproject.toml', encoding='utf8') as pyproject_file:
    for line in takewhile(lambda _: __description__ is None, pyproject_file):
        __description__ = (
            __description__ if __description__ is not None else get_from_line_and_pattern(line, DESCRIPTION_PATTERN)
        )
