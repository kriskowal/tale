
from people import Human, Male, Person
from aliens import Vulcan

__all__ = [
    'Philosopher',
    'Plato',
    'Socrates',
    'Spock',
]


class Philosopher(Person):
    pass

class Plato(Philosopher, Human):
    gender = Male

class Socrates(Philosopher, Human):
    gender = Male

class Spock(Philosopher, Vulcan):
    pass

if __name__ == '__main__':

    from engine import *

    socrates = Socrates()
    plato = Plato()
    me = Person()

    narrate = socrates.narrate(me).narrate_event
    print narrate(Kick(socrates, me))

    narrate = me.narrate(me).narrate_event
    print narrate(Kick(plato, socrates))

