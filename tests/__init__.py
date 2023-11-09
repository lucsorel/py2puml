from itertools import takewhile
from pathlib import Path
from re import compile as re_compile

# exports the version and the project description read from the pyproject.toml file
__version__ = None
__description__ = None

TESTS_PATH = Path(__file__).parent
PROJECT_PATH = TESTS_PATH.parent

VERSION_PATTERN = re_compile('^version = "([^"]+)"$')
DESCRIPTION_PATTERN = re_compile('^description = "([^"]+)"$')


def get_from_line_and_pattern(content_line: str, pattern) -> str:
    pattern_match = pattern.search(content_line)
    if pattern_match is None:
        return None
    else:
        return pattern_match.group(1)


with open(PROJECT_PATH / 'pyproject.toml', encoding='utf8') as pyproject_file:
    for line in takewhile(lambda _: __version__ is None or __description__ is None, pyproject_file):
        __version__ = __version__ if __version__ is not None else get_from_line_and_pattern(line, VERSION_PATTERN)
        __description__ = (
            __description__ if __description__ is not None else get_from_line_and_pattern(line, DESCRIPTION_PATTERN)
        )
