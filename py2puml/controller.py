"""
cases
- domain path does not exist -> error
- domain path is None -> domain path is the current working directory
- domain path is a folder / package -> inspect package (recursive)
  - if domain namespace is None
    - domain namespace is the diff between current working directory and domain path
- domain path is a file / module -> inspect module
- if domain namespace is None
  - domain namespace is the diff between current working directory and domain path
"""

from argparse import ArgumentParser
from contextlib import contextmanager
from pathlib import Path
from sys import path, stdout
from typing import Generator, Protocol, Sequence, TextIO

from py2puml.domain.inspection import Inspection
from py2puml.inspector import Inspector


class InspectorArgs(Protocol):
    path: Path = None
    namespace: str = None
    output_file: Path = None


class InspectorController:
    def _parse_args(self, args: Sequence[str] = None) -> InspectorArgs:
        argparser = ArgumentParser(description='Generate PlantUML class diagrams to document your Python application.')

        argparser.add_argument('-v', '--version', action='version', version='py2puml 0.10.0')
        argparser.add_argument(
            '-p', '--path', metavar='path', type=Path, help='the filepath to the domain to inspect', default=None
        )
        argparser.add_argument(
            '-n',
            '--namespace',
            metavar='namespace',
            type=str,
            help='the namespace of the domain to inspect',
            default=None,
        )
        argparser.add_argument(
            '-o',
            '--output_file',
            metavar='output_file',
            type=Path,
            help='outputs the PlantUML contents in a file if defined, or in the standard output otherwise',
            default=None,
        )

        return argparser.parse_args(args)

    @contextmanager
    def _open_output(self, output_file: Path = None) -> Generator[TextIO, None, None]:
        if output_file is None:
            yield stdout
        else:
            with open(output_file, 'w', encoding='utf-8') as plantuml_file:
                yield plantuml_file

    def inspect(self):
        # adds the current working directory to the system path in the first place
        # to ease module resolution when py2puml imports them
        current_working_directory = Path.cwd().resolve()
        path.insert(0, str(current_working_directory))

        args = self._parse_args()

        # inspects the current working directory if no path is specified
        root_domain_path = args.path or current_working_directory

        # eases the default case where the domain namespace is the relative namespace
        # between the inspected path and the current working directory
        if args.namespace is None:
            namespace_relative_path = root_domain_path.resolve().relative_to(current_working_directory)
            root_domain_namespace = '.'.join(namespace_relative_path.parts)
        else:
            root_domain_namespace = args.namespace

        self._check_domain_path_and_namespace_consistency(root_domain_path, root_domain_namespace)

        with self._open_output(args.output_file) as output_io:
            for plantuml_line in Inspector(root_domain_path, root_domain_namespace).inspect(Inspection({}, [])):
                output_io.write(plantuml_line)

    def _check_domain_path_and_namespace_consistency(self, root_domain_path: Path, root_domain_namespace: str):
        namespace_parts = root_domain_namespace.split('.') if root_domain_namespace else ()
        for from_end_index, (path_part, namespace_part) in enumerate(
            zip(reversed(root_domain_path.parts), reversed(namespace_parts))
        ):
            if path_part != namespace_part:
                namespace = '.'.join(root_domain_namespace)
                subpath = '/'.join(root_domain_path.parts[:-from_end_index])
                path_and_namespace_error = f"the namespace part '{namespace_part}' of namespace '{namespace}' does not match subpath '{subpath}' of '{str(root_domain_path)}'"
                raise ValueError(path_and_namespace_error)


if __name__ == '__main__':
    InspectorController().inspect()
