
from animals import Animal

__all__ = [
    'Insect',
    'FlyingInsect',
    'Ant',
    'Fly',
    'Gnat',
    'Bee',
    'Bufferfly',
]

class Insect(Animal):
    pass

class Ant(Insect):
    collective = 'army'

class Flea(Insect):
    pass

class FlyingInsect(Insect):
    collective = 'swarm'
    
class Fly(FlyingInsect):
    collective = 'business'

class Gnat(FlyingInsect):
    collective = 'cloud'

class Bee(FlyingInsect):
    collective = 'swarm'

class Bufferfly(FlyingInsect):
    pass

