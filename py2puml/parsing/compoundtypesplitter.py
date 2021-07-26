
from re import compile, Pattern
from typing import List, Tuple

IS_COMPOUND_TYPE: Pattern = compile('^[a-z|A-Z|\\[|\\]|\\.|,|\\s|_]+$')
SPLITTING_CHARACTERS = ('[', ']', ',')

class CompoundTypeSplitter(object):
    def __init__(self, compound_type_annotation: str):
        if (compound_type_annotation is None) or not IS_COMPOUND_TYPE.match(compound_type_annotation):
            raise ValueError(f'{compound_type_annotation} seems to be an invalid type annotation')

        self.compound_type_annotation = compound_type_annotation
    
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
