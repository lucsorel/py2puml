from dataclasses import dataclass

@dataclass
class UmlComposition(object):
    compound_fqdn: str
    component_fqdn: str
