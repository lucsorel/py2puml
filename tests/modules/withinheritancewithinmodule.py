from dataclasses import dataclass


@dataclass
class Animal:
    has_notochord: bool


@dataclass
class Fish(Animal):
    fins_number: int


@dataclass
class Light:
    luminosity_max: float


@dataclass
class GlowingFish(Fish, Light):
    glow_for_hunting: bool
    glow_for_mating: bool
