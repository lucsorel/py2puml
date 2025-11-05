from pathlib import Path
from typing import Iterator

from py2puml.domain.inspection import Inspection
from py2puml.inspector import Inspector


def py2puml(domain_path: str, domain_module: str, inspection_working_directory: Path = None) -> Iterator[str]:
    # uses the current working directory by default:
    if inspection_working_directory is None:
        inspection_working_directory = Path.cwd().resolve()

    yield from Inspector(inspection_working_directory, Path(domain_path), domain_module).inspect(Inspection({}, []))
