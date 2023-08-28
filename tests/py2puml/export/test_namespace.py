from typing import Dict, List, Tuple

from pytest import mark

from py2puml.domain.package import Package
from py2puml.domain.umlitem import UmlItem
from py2puml.domain.umlrelation import UmlRelation
from py2puml.export.namespace import build_packages_structure, get_or_create_module_package, visit_package
from py2puml.inspection.inspectpackage import inspect_package


@mark.parametrize(
    ['root_package', 'module_qualified_name'], [
        (Package(None), 'py2puml'),
        (Package(None, [Package('py2puml')]), 'py2puml'),
        (Package(None), 'py2puml.export.namespace'),
    ]
)
def test_get_or_create_module_package(root_package: Package, module_qualified_name: str):
    module_parts = module_qualified_name.split('.')
    module_package = get_or_create_module_package(root_package, module_parts)
    assert module_package.name == module_parts[-1], 'the module package has the expected name'

    # checks that the hierarchy of intermediary nested packages has been created if necessary
    inner_package = root_package
    for module_name in module_parts:
        inner_package = next(
            child_package for child_package in inner_package.children if child_package.name == module_name
        )

    assert inner_package == module_package, f'the module package is contained in the {module_qualified_name} hierarchy'


@mark.parametrize(
    ['uml_items', 'items_number_by_package_name'], [
        ([UmlItem('Package', 'py2puml.export.namespace.Package')], {
            'namespace': 1
        }),
        (
            [
                UmlItem('UmlClass', 'py2puml.domain.umlclass.UmlClass'),
                UmlItem('UmlAttribute', 'py2puml.domain.umlclass.UmlAttribute')
            ], {
                'umlclass': 2
            }
        ),
        (
            [
                UmlItem('Package', 'py2puml.export.namespace.Package'),
                UmlItem('ImaginaryClass', 'py2puml.domain.ImaginaryClass'),
                UmlItem('UmlClass', 'py2puml.domain.umlclass.UmlClass'),
                UmlItem('UmlAttribute', 'py2puml.domain.umlclass.UmlAttribute')
            ], {
                'domain': 1,
                'namespace': 1,
                'umlclass': 2
            }
        ),
    ]
)
def test_build_packages_structure(uml_items: List[UmlItem], items_number_by_package_name: Dict[str, int]):
    root_package = build_packages_structure(uml_items)

    # ensures that:
    # - each uml_item has a package for its module
    # - each nested package either has module items or child packages
    for uml_item in uml_items:
        inner_package = root_package
        module_parts = uml_item.fqn.split('.')[:-1]
        for module_name in module_parts:
            inner_package = next(
                child_package for child_package in inner_package.children if child_package.name == module_name
            )

            expected_items_number = items_number_by_package_name.get(module_name, 0)
            assert expected_items_number == inner_package.items_number, f'package {module_name} must have {expected_items_number} items, found {inner_package.items_number}'

            has_children_packages = len(inner_package.children) > 0
            has_module_items = inner_package.items_number > 0
            assert has_children_packages or has_module_items, f'package {inner_package.name} in hierarchy of {module_parts} has items or children packages'


NO_CHILDREN_PACKAGES = []

SAMPLE_ROOT_PACKAGE = Package(
    None, [
        Package(
            'py2puml', [
                Package(
                    'domain',
                    [Package('package', NO_CHILDREN_PACKAGES, 1),
                     Package('umlclass', NO_CHILDREN_PACKAGES, 1)]
                ),
                Package('inspection', [Package('inspectclass', NO_CHILDREN_PACKAGES, 1)])
            ]
        )
    ]
)
SAMPLE_NAMESPACE_LINES = '''namespace py2puml {
  namespace domain {
    namespace package {}
    namespace umlclass {}
  }
  namespace inspection.inspectclass {}
}'''


@mark.parametrize(
    ['package_to_visit', 'parent_namespace_names', 'indentation_level', 'expected_namespace_lines'],
    [
        (Package(None), (), 0, []),  # the root package yields no namespace documentation
        (Package(None, NO_CHILDREN_PACKAGES, 1),
         (), 0, ['namespace  {}\n']),  # the root package yields namespace documentation if it has uml items
        (Package(None, NO_CHILDREN_PACKAGES, 1), (), 1, ['  namespace  {}\n']),  # indentation level of 1 -> 2 spaces
        (Package(None, NO_CHILDREN_PACKAGES, 1),
         (), 3, ['      namespace  {}\n']),  # indentation level of 3 -> 6 spaces
        (
            Package('umlclass', NO_CHILDREN_PACKAGES, 2),
            ('py2puml', 'domain'), 0, ['namespace py2puml.domain.umlclass {}\n']
        ),
        (SAMPLE_ROOT_PACKAGE, (), 0, (f'{line}\n' for line in SAMPLE_NAMESPACE_LINES.split('\n'))),
    ]
)
def test_visit_package(
    package_to_visit: Package, parent_namespace_names: Tuple[str], indentation_level: int,
    expected_namespace_lines: List[str]
):
    for expected_namespace_line, namespace_line in zip(expected_namespace_lines, visit_package(
            package_to_visit, parent_namespace_names, indentation_level)):
        assert expected_namespace_line == namespace_line


def test_build_packages_structure_visit_package_from_tree_package(
    domain_items_by_fqn: Dict[str, UmlItem], domain_relations: List[UmlRelation]
):
    domain_path = 'tests/modules/withnestednamespace'
    domain_module = 'tests.modules.withnestednamespace'
    inspect_package(domain_path, domain_module, domain_items_by_fqn, domain_relations)
    package = build_packages_structure(domain_items_by_fqn.values())

    with open(f'{domain_path}/plantuml_namespace.txt', encoding='utf8') as tree_namespace_file:
        for line_index, (namespace_line, expected_namespace_line) in enumerate(zip(visit_package(package, (), 0),
                                                                                   tree_namespace_file)):
            assert namespace_line == expected_namespace_line, f'{line_index}: namespace content'
