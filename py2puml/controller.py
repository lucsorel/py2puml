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
from sys import stdout
from typing import Generator, Protocol, Sequence, TextIO
from warnings import warn

from py2puml.domain.inspection import Inspection
from py2puml.inspector import Inspector


class InspectorArgs(Protocol):
    path: Path = None
    namespace: str = None
    output_file: Path = None


class InspectorController:
    def _parse_args(self, args: Sequence[str] = None) -> InspectorArgs:
        argparser = ArgumentParser(description='Generate PlantUML class diagrams to document your Python application.')

        argparser.add_argument('-v', '--version', action='version', version='py2puml 0.11.0')

        # deprecated positional arguments
        argparser.add_argument(
            'deprecated_path',
            nargs='?',
            type=Path,
            metavar='path',
            help='the filepath to the domain to inspect - deprecated: use --path path/to/module... instead',
            default=None,
        )
        argparser.add_argument(
            'deprecated_namespace',
            nargs='?',
            metavar='namespace',
            help='the namespace of the domain to inspect - deprecated: use --namespace package.to.module instead',
            default=None,
        )

        # optional arguments
        argparser.add_argument(
            '-p',
            '--path',
            metavar='path',
            type=Path,
            help='the filepath to the domain to inspect. Use the current working directory as the root of the domain if unspecified',
            default=None,
        )
        argparser.add_argument(
            '-n',
            '--namespace',
            metavar='namespace',
            help='the namespace of the domain to inspect. Use the current working directory',
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

        args = argparser.parse_args(args)

        # adapts the old cli arguments if any
        if args.deprecated_path or args.deprecated_namespace:
            deprecation_message_parts = [
                'Deprecation warning: specify the path to inspect and its corresponding namespace with specific flags',
                f'Use `py2puml --path {args.deprecated_path} --namespace {args.deprecated_namespace}` instead',
                'Type py2puml --help for more details about the available flags.',
            ]
            args.path = args.deprecated_path
            args.namespace = args.deprecated_namespace

            warn('. '.join(deprecation_message_parts), DeprecationWarning, stacklevel=1)

        # remove deprecated arguments from the returned namespace
        delattr(args, 'deprecated_path')
        delattr(args, 'deprecated_namespace')

        return args

    @contextmanager
    def _open_output(self, output_file: Path = None) -> Generator[TextIO, None, None]:
        if output_file is None:
            yield stdout
        else:
            with open(output_file, 'w', encoding='utf-8') as plantuml_file:
                yield plantuml_file

    def inspect(self, args: Sequence[str] = None):
        parsed_args = self._parse_args(args)

        # inspects the current working directory if no path is specified
        current_working_directory = Path.cwd().resolve()
        root_domain_path = parsed_args.path or current_working_directory

        # eases the default case where the domain namespace is the relative namespace
        # between the inspected path and the current working directory
        if parsed_args.namespace is None:
            namespace_relative_path = root_domain_path.resolve().relative_to(current_working_directory)
            if root_domain_path.is_dir():
                namespace_parts = namespace_relative_path.parts
            else:
                namespace_parts = [*namespace_relative_path.parent.parts, namespace_relative_path.stem]
            root_domain_namespace = '.'.join(namespace_parts)
        else:
            root_domain_namespace = parsed_args.namespace
            self._check_domain_path_and_namespace_consistency(root_domain_path, root_domain_namespace)

        with self._open_output(parsed_args.output_file) as output_io:
            for plantuml_line in Inspector(root_domain_path, root_domain_namespace).inspect(Inspection({}, [])):
                output_io.write(plantuml_line)

    def _check_domain_path_and_namespace_consistency(self, root_domain_path: Path, root_domain_namespace: str) -> bool:
        namespace_parts = root_domain_namespace.split('.') if root_domain_namespace else ()
        if root_domain_path.is_file():
            root_domain_path_parts = [*root_domain_path.parent.parts, root_domain_path.stem]
        else:
            root_domain_path_parts = root_domain_path.parts

        for from_end_index, (path_part, namespace_part) in enumerate(
            zip(reversed(root_domain_path_parts), reversed(namespace_parts))
        ):
            if path_part != namespace_part:
                subpath = '/'.join(root_domain_path.parts[:-from_end_index])
                path_and_namespace_error = f"the namespace part '{namespace_part}' of namespace '{root_domain_namespace}' does not match subpath '{subpath}' of '{str(root_domain_path)}'"
                raise ValueError(path_and_namespace_error)

        return True
