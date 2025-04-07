from importlib import import_module
from inspect import getabsfile, isclass
from pathlib import Path
from pkgutil import walk_packages
from types import ModuleType
from typing import Dict, Iterator, Tuple, Type

from py2puml.domain.inspection import Inspection
from py2puml.export.puml import to_puml_content
from py2puml.inspection.inspectmodule import inspect_domain_definition


class Inspector:
    def __init__(self, root_domain_path: Path, root_domain_namespace: str):
        self.root_domain_path = root_domain_path.resolve()
        self.root_domain_namespace = root_domain_namespace
        self.filtered_definitions: Dict[str, bool] = {}

    def inspect(self, inspection: Inspection) -> Iterator[str]:
        if self.root_domain_path.is_dir():
            self._inspect_package(self.root_domain_path, self.root_domain_namespace, inspection)
        else:
            self._inspect_module(self.root_domain_path, self.root_domain_namespace, inspection)

        for puml_line in to_puml_content(
            self.root_domain_namespace if self.root_domain_namespace else self.root_domain_path.name,
            inspection.items_by_fqn.values(),
            inspection.relations,
        ):
            yield puml_line
        # yield f"' {inspection=}\n"

    def _inspect_package(self, domain_path: Path, root_domain_namespace: str, inspection: Inspection):
        # inspects the packages module and inner packages
        root_domain_namespace_prefix = f'{root_domain_namespace}.' if root_domain_namespace else ''
        for _, name, is_pkg in walk_packages([str(domain_path)], root_domain_namespace_prefix):
            module_name = f'{name}.__init__' if is_pkg else name
            self._inspect_module(module_name, inspection)

    def _inspect_module(self, module_name: str, inspection: Inspection):
        # print(f'inspecting module {module_name}')
        module_to_inspect = import_module(module_name)
        for _, definition in self._filter_module_definitions(module_to_inspect):
            # print(definition_fqn, definition)
            inspect_domain_definition(
                definition, self.root_domain_namespace, inspection.items_by_fqn, inspection.relations
            )

    def _filter_module_definitions(self, module_to_inspect: ModuleType) -> Iterator[Tuple[str, Type]]:
        for definition in vars(module_to_inspect).values():
            if isclass(definition):
                try:
                    definition_file = getabsfile(definition)
                # skips builtins
                except TypeError:
                    pass
                else:
                    # this fqn can start with "__main__" instead of the real fqn
                    definition_fqn = f'{definition.__module__}.{definition.__qualname__}'
                    yield_definition = self.filtered_definitions.get(definition_fqn)
                    if yield_definition is None:
                        try:
                            relative_path = Path(definition_file).relative_to(self.root_domain_path)
                        except ValueError:
                            pass
                            self.filtered_definitions[definition_fqn] = False
                        else:
                            definition_namespace = (
                                tuple(self.root_domain_namespace.split('.'))
                                if self.root_domain_namespace
                                else () + relative_path.parts
                            )
                            definition_static_fqn = f'{".".join(definition_namespace)}.{definition.__qualname__}'

                            # filters on the specified namespace if any, or on the source filepath of the definition
                            if self.root_domain_namespace:
                                yield_definition = definition_static_fqn.startswith(self.root_domain_namespace)
                            else:
                                yield_definition = Path(definition_file).is_relative_to(self.root_domain_path)

                            self.filtered_definitions[definition_fqn] = yield_definition

                            if yield_definition:
                                yield definition_static_fqn, definition
