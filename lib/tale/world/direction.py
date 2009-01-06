
from tale.world.things import Thing

class DirectionMetaclass(Thing.__metaclass__):
    def __init__(self, name, bases, attys):
        super(DirectionMetaclass, self).__init__(name, bases, attys)
        self.directions[name.lower()] = self()

class Direction(Thing):
    __metaclass__ = DirectionMetaclass
    directions = {}

class North(Direction): pass
class South(Direction): pass
class East(Direction): pass
class West(Direction): pass

