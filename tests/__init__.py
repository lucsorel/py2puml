from os.path import dirname, realpath, join
from re import compile
from itertools import takewhile

# exports the version and the project description read from the pyproject.toml file
__version__ = None
__description__ = None

PARENT_DIR = dirname(dirname(realpath(__file__)))
VERSION_PATTERN = compile('^version = "([^"]+)"$')
DESCRIPTION_PATTERN = compile('^description = "([^"]+)"$')

def get_from_line_and_pattern(line: str, pattern) -> str:
    pattern_match = pattern.search(line)
    if pattern_match is None:
        return None
    else:
        return pattern_match.group(1)

with open(join(PARENT_DIR, 'pyproject.toml')) as pyproject:
    for line in takewhile(lambda _: __version__ is None or __description__ is None, pyproject):
        __version__ = __version__ if __version__ is not None else get_from_line_and_pattern(line, VERSION_PATTERN)
        __description__ = __description__ if __description__ is not None else get_from_line_and_pattern(line, DESCRIPTION_PATTERN)
