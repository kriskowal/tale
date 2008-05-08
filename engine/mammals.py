
from animals import Animal

__all__ = [
    'Mammal',
    'Cat',
    'Dog',
    'Cow',
]

class Mammal(Animal):
    pass

class Cat(Mammal):
    collective = 'herd'

class Dog(Mammal):
    pass

class Cow(Mammal):
    plural = 'cattle'
    collective = 'herd'

class SeaMammal(Mammal):
    collective = 'pod'

class Manatee(SeaMammal):
    pass

class Dolphin(SeaMammal):
    pass

class Whale(SeaMammal):
    pass

class Narwhal(Whale):
    pass

