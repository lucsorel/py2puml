
class Animal(object):
    has_notochord: bool

class Fish(Animal):
    fins_number: int

class Light(object):
    luminosity_max: float

class GlowingFish(Fish, Light):
    glow_for_hunting: bool
    glow_for_mating: bool
