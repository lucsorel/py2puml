from typing import Iterable, List, Tuple

from py2puml.domain.package import Package
from py2puml.domain.umlitem import UmlItem


# templating constants
INDENT = '  '
PUML_NAMESPACE_START_TPL = '{indentation}namespace {namespace_name} {{'
PUML_NAMESPACE_END_TPL = '{indentation}}}\n'


def get_or_create_module_package(root_package: Package, domain_parts: List[str]) -> Package:
    '''Returns or create the package containing the tail domain part'''
    package = root_package
    for domain_part in domain_parts:
        domain_package = next((
            sub_package for sub_package in package.children
            if sub_package.name == domain_part
        ), None)
        if domain_package is None:
            domain_package = Package(domain_part)
            package.children.append(domain_package)
        package = domain_package
    return package

def visit_package(package: Package, parent_namespace_names: Tuple[str], indentation_level: int) -> Iterable[str]:
    '''
    Recursively visits the package and its subpackages to produce the PlantUML documentation about the namespace
    '''
    package_with_items = package.items_number > 0
    # prints the namespace if:
    # - it has inner uml_items
    # - OR it has more than one sub-package (if no item and only 1 subpackage, they can be concatenated)
    print_namespace = package_with_items or len(package.children) > 1
    # the indentation for the inner namespace is incremented if the current namespace is printed (because it has uml_items in it)
    # otherwise its package name will be used as a prefix for the inner namespaces
    next_indentation = indentation_level + 1 if print_namespace else indentation_level
    package_with_name = package.name is not None
    namespace_names = parent_namespace_names

    # concatenates the package name with the ones of the empty parent parent names
    if package_with_name:
        namespace_names += (package.name,)

    # starts the namespace declaration (without an end-of-line line return, we don't know yet whether there is inner content)
    start_of_namespace_line = None
    if print_namespace:
        # initializes the namespace decalaration but not yield yet: we don't know if it should be closed now or if there is inner content
        start_of_namespace_line = PUML_NAMESPACE_START_TPL.format(
            indentation=INDENT * indentation_level,
            namespace_name='.'.join(namespace_names)
        )

    parent_names = () if print_namespace else namespace_names
    has_inner_namespace = False
    for sub_package in package.children:
        for sub_package_line in visit_package(sub_package, parent_names, next_indentation):
            if not has_inner_namespace:
                has_inner_namespace = True
                # ends the start-of-namespace with a line return because some inner namespace is about to be documented
                if print_namespace:
                    yield f'{start_of_namespace_line}\n'
            yield sub_package_line

    # yields the end-of-namespace brace:
    # - with an indentation if it had sub-packages
    # - right after the opening brace otherwise
    if print_namespace:
        if has_inner_namespace:
            yield PUML_NAMESPACE_END_TPL.format(indentation=INDENT * indentation_level)
        else:
            yield PUML_NAMESPACE_END_TPL.format(indentation=start_of_namespace_line)

def build_packages_structure(uml_items: List[UmlItem]) -> Package:
    '''
    Creates the Package arborescent structure with the given UML items with their fully-qualified module names
    '''
    root_package = Package(None)
    for uml_item in uml_items:
        module_package = get_or_create_module_package(root_package, uml_item.fqn.split('.')[:-1])
        module_package.items_number += 1

    return root_package

def puml_namespace_content(uml_items: List[UmlItem]) -> Iterable[str]:
    '''
    Yields the documentation about the packages structure in the PlantUML syntax
    '''
    root_package = Package(None)
    # creates the Package arborescent structure with the given UML items with their fully-qualified module names
    for uml_item in uml_items:
        class_package = get_or_create_module_package(root_package, uml_item.fqn.split('.')[:-1])
        class_package.items_number += 1

    # yields the documentation using a visitor pattern approach
    for namespace_line in visit_package(root_package, (), 0):
        yield f"{namespace_line}"
