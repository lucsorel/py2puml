from sys import argv
from typing import NamedTuple

from withrootscriptandsrc.argshandler import ArgsHandler


class Args(NamedTuple):
    arg1: str = None
    arg2: str = None
    arg3: str = None


if __name__ == '__main__':
    args: Args = Args(*argv)
    ArgsHandler(*args).handle_args()
