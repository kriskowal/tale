#!/usr/bin/env PYTHONPATH=.. python

from world import Sheep, Thing, Unique, Event, Explode, Tick, Tock,\
    Materialize, Move, Person, Male, Female, Enter
from narrate import Narrative, Narrator

from time import sleep
from weakref import proxy
from itertools import chain
import datetime
from traverse import postfix

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
            yield Enter(sheep, self.children[0])
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

def simd():
    try:
        while True:
            context = Context(time = datetime.datetime.now(),)
            print narrative(postfix(world, tick, context))
            sleep(1)
    except KeyboardInterrupt:
        pass
     
