
from creatures import Creature, GenderNamed, Male, Female
from weakproperty import WeakProperty

class Person(Creature):

    def get_name(self):
        return getattr(self, '_name', None)
    def set_name(self, name):
        self._name = name
    name = property(get_name, set_name)

    singular = 'person'
    plural = 'people'
    collective = 'group'

    mother = WeakProperty()
    father = WeakProperty()

class Human(GenderNamed, Person):

    singular_male = 'man'
    singular_female = 'woman'

    plural_male = 'men'
    plural_female = 'women'

