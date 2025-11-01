from pathlib import Path
from typing import Iterator

from py2puml.domain.inspection import Inspection
from py2puml.inspector import Inspector


def py2puml(domain_path: str, domain_module: str) -> Iterator[str]:
    yield from Inspector(Path.cwd().resolve(), Path(domain_path), domain_module).inspect(Inspection({}, []))
