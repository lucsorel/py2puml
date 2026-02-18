from dataclasses import dataclass

from withrootscriptandsrc.argshandler import ArgsHandler


@dataclass
class RootTool:
    command: str
    handler: ArgsHandler
