from re import Pattern
from re import compile as re_compile
from typing import Tuple

# a class name wrapped by ForwardRef(...)
FORWARD_REFERENCES: Pattern = re_compile(r"ForwardRef\('([^']+)'\)")

# valid characters for class names and compound types
IS_COMPOUND_TYPE: Pattern = re_compile(r'^[a-z|A-Z|0-9|\[|\]|\.|,|\s|_|\|]+$')

# characters involved in the build-up of compound types
SPLITTING_CHARACTERS = '[', ']', ',', '|'

# 'None' in 'Union[str, None]' type signature is changed into 'NoneType' when inspecting a module
LAST_NONETYPE_IN_UNION: Pattern = re_compile(r'Union\[(?:(?:[^\[\]])*NoneType)')


def remove_forward_references(compound_type_annotation: str, module_name: str) -> str:
    """
    Removes the forward reference mention from the string representation of a type annotation.
    This happens when a class attribute refers to the class being defined (where Person.friends is of type List[Person])
    The type which is referred to is prefixed by the module where it is defined to help resolution.
    """
    return (
        None
        if compound_type_annotation is None
        else FORWARD_REFERENCES.sub(f'{module_name}.\\1', compound_type_annotation)
    )


def replace_nonetype_occurrences_in_union_types(type_annotation: str) -> str:
    """
    `None` types are replaced by `NoneType` during code inspection in type annotations like `Union[str, None]`.
    This function replaces back the `NoneType` occurrences to `None`
    See https://bugs.python.org/issue44635
    """
    if type_annotation is None:
        return None

    cleaned_type_annotation = type_annotation

    while (union_match_clauses := list(LAST_NONETYPE_IN_UNION.finditer(cleaned_type_annotation))) and len(
        union_match_clauses
    ) > 0:
        union_last_match_clause = union_match_clauses[-1]
        match_start, match_end = union_last_match_clause.span()
        cleaned_type_annotation = (
            cleaned_type_annotation[0 : match_end - 8] + 'None' + cleaned_type_annotation[match_end:]
        )

    return cleaned_type_annotation


class CompoundTypeSplitter:
    """
    Splits the representation of a compound type annotation into a list of:
    - its components (that can be resolved against the module where the type annotation was found)
    - its structuring characters: '[', ']' and ','
    """

    def __init__(self, compound_type_annotation: str, module_name: str):
        resolved_type_annotations = remove_forward_references(compound_type_annotation, module_name)
        resolved_type_annotations = replace_nonetype_occurrences_in_union_types(resolved_type_annotations)
        if (resolved_type_annotations is None) or not IS_COMPOUND_TYPE.match(resolved_type_annotations):
            raise ValueError(f'{compound_type_annotation} seems to be an invalid type annotation')

        self.compound_type_annotation = resolved_type_annotations

    def get_parts(self) -> Tuple[str]:
        "Iteratively splits the type annotation with the different SPLITTING_CHARACTERS"

        parts = [self.compound_type_annotation]
        for splitting_character in SPLITTING_CHARACTERS:
            new_parts = []
            for part in parts:
                splitted_parts = part.split(splitting_character)
                new_parts.append(splitted_parts[0])
                # some splitting characters (like ',' and '|' and '[') separate a type annotation into different types
                # others (like ']') must just be separated from the text
                if len(splitted_parts) > 1:
                    for splitted_part in splitted_parts[1:]:
                        new_parts.extend([splitting_character, splitted_part])
            parts = (new_part.strip() for new_part in new_parts if len(new_part.strip()) > 0)

        return tuple(parts)
