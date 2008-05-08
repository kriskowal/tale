
from creatures import Creature, GenderNamed, Male, Female

__all__ = [
    'Person',
    'Human',
    'Player',
    'Person',
    'Soul',
]


class Person(Creature):

    @property
    def name(self):
        return self.__class__.__name__

    singular = 'person'
    plural = 'people'
    collective = 'group'

    def narrate(self, audience):
        from narrate import Narration
        return Narration(self, audience)

class Human(GenderNamed):

    singular_male = 'man'
    singular_female = 'woman'

    plural_male = 'men'
    plural_female = 'women'

# mixin
class Player(object):
    pass

class Soul(Person):
    pass

creator = Player()
soul_of_creator = Soul(of = creator)

