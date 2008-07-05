
from tale.engine.mammals import Sheep
from tale.engine.things import Thing, Unique
from tale.engine.events import Event, Explode, Tick, Tock, Materialize, Move
from tale.engine.people import Person, Male, Female
from tale.engine.narrate import Narrative, Narrator

from time import sleep
from weakref import proxy
from itertools import chain
import datetime

class Context(object):
    def __init__(self, parent = None, **kws):
        if parent is not None:
            for key, value in vars(parent).items():
                setattr(self, key, value)
        for key, value in kws.items():
            setattr(self, key, value)

class SuicideSheep(Sheep):
    singular = 'sheep'
    def tick(self, context):
        for event in super(SuicideSheep, self).tick(context):
            yield event
        from random import randint
        if randint(0, 2) == 0:
            yield Explode(self)

class Room(Thing):

    def __init__(self, parent = None, children = None, things = None):
        super(Room, self).__init__()
        if children is None: children = []
        if things is None: things = set()
        if parent is not None: parent = proxy(parent)
        self.parent = parent
        self.children = children
        self.things = things

    def __iter__(self):
        return chain(
            iter(self.children),
            iter(self.things),
        )

    def get_children(self):
        return self._children
    def set_children(self, children):
        for child in children:  
            child.parent = self
        self._children = children
    children = property(get_children, set_children)

class World(Room, Unique):
    def __init__(self):
        super(World, self).__init__(children = (
            Room(),
            Room(),
            Room(),
            Room(),
        ))

    def tick(self, context):
        yield Tick(self)
        if context.time.second % 3 == 0:
            sheep = SuicideSheep()
            yield Materialize(sheep)
            yield Move(sheep, to = self.children[0])
        yield Tock(self)

world = World()
narrator = Narrator()
you = Person()
narrative = Narrative(narrator, you)

def tick(self, context):
    context = Context(context, room = self)
    for event in self.tick(context):
        yield event
        for subevent in drive(event, context):
            yield subevent
    for thing in list(self):
        for event in thing.tick(context):
            yield event
            for subevent in drive(event, context):
                yield subevent

def drive(event, context):
    events = event.tick(context)
    if events is not None:
        for event in events:
            for subevent in drive(event, context):
                yield subevent

def traversal(root, pre = False, post = False):
    if pre:
        yield root
    for child in root.children:
        for room in traversal(child, pre, post):
            yield room
    if post:
        yield root

def postfix_visit(root, function, *args, **kws):
    for room in traversal(root, post = True):
        for event in function(room, *args, **kws):
            yield event

def simd():
    while True:
        context = Context(time = datetime.datetime.now(),)
        print narrative.narrate_events(postfix_visit(world, tick, context))
        sleep(1)

