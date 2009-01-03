
from animals import Animal

__all__ = [
    'Mammal',
    'Cat',
    'Dog',
    'Cow',
]

class Mammal(Animal):
    pass

class Canine(Mammal):
    collective = 'pack'

class Dog(Canine):
    pass

class Wolf(Canine):
    plural = 'wolves'

class Fox(Canine):
    pass

class Felid(Mammal):
    plural = 'felida'

class Cat(Felid):
    collective = 'herd'

class Kitten(Cat):
    collective = 'kit'

class Panther(Felid):
    pass

class Lion(Panther):
    collective = 'pride'

class Tiger(Panther):
    pass

class Leopard(Panther):
    pass

class Jaguar(Panther):
    pass

class Bovid(Mammal):
    collective = 'herd'

class Cow(Bovid):
    plural = 'cattle'
    singular_male = 'bull'

class Ox(Cow):
    plural = 'oxen'

class Bear(Mammal):
    collective = 'sleuth'

class Sheep(Mammal):
    plural = 'flock'

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

