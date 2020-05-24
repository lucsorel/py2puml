from os.path import dirname, realpath, join
from re import compile, Match

# exports the version read from the pyproject.toml file
try:
    PARENT_DIR = dirname(dirname(realpath(__file__)))
    VERSION_PATTERN = compile('^version = "([^"]+)"$')
    with open(join(PARENT_DIR, 'pyproject.toml')) as pyproject:
        version_match: Match = next((
            match for match in (VERSION_PATTERN.search(line) for line in pyproject.readlines())
            if match is not None
        ), None)

        __version__ = version_match.group(1)
except:
    __version__ = None

