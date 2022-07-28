
from re import compile as re_compile, Pattern
from typing import Tuple


FORWARD_REFERENCES: Pattern = re_compile(r"ForwardRef\('([^']+)'\)")
IS_COMPOUND_TYPE: Pattern = re_compile(r'^[a-z|A-Z|0-9|\[|\]|\.|,|\s|_]+$')
SPLITTING_CHARACTERS = ('[', ']', ',')


def remove_forward_references(compound_type_annotation: str, module_name: str) -> str:
    '''
    Removes the forward reference mention from the string representation of a type annotation.
    This happens when a class attribute refers to the class being defined (where Person.friends is of type List[Person])
    The type which is referred to is prefixed by the module where it is defined to help resolution.
    '''
    return None if compound_type_annotation is None else FORWARD_REFERENCES.sub(f'{module_name}.\\1', compound_type_annotation)

class CompoundTypeSplitter:
    '''
    Splits the representation of a compound type annotation into a list of:
    - its components (that can be resolved against the module where the type annotation was found)
    - its structuring characters: '[', ']' and ','
    '''
    def __init__(self, compound_type_annotation: str, module_name: str):
        resolved_type_annotations = remove_forward_references(compound_type_annotation, module_name)
        if (resolved_type_annotations is None) or not IS_COMPOUND_TYPE.match(resolved_type_annotations):
            raise ValueError(f'{compound_type_annotation} seems to be an invalid type annotation')

        self.compound_type_annotation = resolved_type_annotations
    
    def get_parts(self) -> Tuple[str]:
        parts = [self.compound_type_annotation]
        for splitting_character in SPLITTING_CHARACTERS:
            new_parts = []
            for part in parts:
                splitted_parts = part.split(splitting_character)
                new_parts.append(splitted_parts[0])
                if len(splitted_parts) > 1:
                    for splitted_part in splitted_parts[1:]:
                        new_parts.extend([splitting_character, splitted_part])
            parts = [
                new_part.strip()
                for new_part in new_parts
                if len(new_part.strip()) > 0
            ]

        return tuple(parts)
