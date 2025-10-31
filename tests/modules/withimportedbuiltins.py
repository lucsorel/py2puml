from builtins import SystemExit


class SystemExitError(SystemExit):
    reason: str
