
from things import Thing
from life import Gene, MetaGenetic

class Male(object): pass
class Female(object): pass

class GenderNamed(object):

    @property
    def singular(self):
        return self.gender is Male and self.singular_male or self.singular_female

    @property
    def pular(self):
        return self.gender is Male and self.plural_male or self.plural_female

class GenderCollectiveNamed(object):

    @property
    def collective(self):
        return self.gender is Male and self.collective_male or self.collective_female


class Creature(Thing):
    def __init__(self, **kws):
        for name, gene in self.genes:
            gene.init()
        for key, value in kws.items():
            setattr(self, key, value)
        self.__class__ = type(self.__class__.__name__, tuple([
            gene.type for name, gene in self.genes
        ] + list(self.__class__.__mro__)), dict(self.__class__.__dict__))
    __metaclass__ = MetaGenetic
    gender = Gene(Male, Female)

class Reproducer(Thing):
    def __init__(self, begets):
        self.begets = begets
        
from animals import *

