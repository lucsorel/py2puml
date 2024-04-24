"""
When attempting to resolve test.range, the python interpreter will search:
- in the current working directory (and should succeed)
- in the test package of the Python standard library (and should fail)

This non-regression test ensures that the current working directory is
in the first position of the paths of PYTHON_PATH (sys.path) so that
module resolution is attempted first in the inspected codebase.
"""

from datetime import datetime


class Range:
    def __init__(self, start: datetime, stop: datetime):
        self.start = start
        self.stop = stop
