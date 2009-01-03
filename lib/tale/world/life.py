
import random
from things import Thing

class Gene(Thing):
    gene_count = 0
    def __init__(self, *types):
        self.types = types
        self.gene_number = self.gene_count
        self.gene_count += 1
    def init(self):
        self.type = random.choice(self.types)
    def __get__(self, creature, Creature):
        return self.type
    def __set__(self, Creature, type):
        self.type = type

class MetaGenetic(type):
    # adds types to an object based on attributes
    def __new__(self, name, bases, attributes):
        genes = sorted(
            (
                (name, gene)
                for name, gene in attributes.items()
                if isinstance(gene, Gene)
            ),
            key = lambda x: x[1].gene_number
        )
        attributes['genes'] = genes
        return type(name, bases, attributes)

