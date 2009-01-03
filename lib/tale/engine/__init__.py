"""
Herein lie things and events.
"""

# Import all classes from this directory
from os import listdir
from os.path import dirname, join, basename
import os
from os.path import *

for module_name in (x[:-3] for x in listdir(dirname(__file__) or '.') if x[-3:] == '.py'):
    if module_name != '__init__':
        __import__(__name__ + '.' + module_name, {}, {}, ('*',))

from events import Event
from things import Thing
events = Event.events
things = Thing.things

from itertools import chain
from sys import modules
__all__ = ['events', 'things', 'Event', 'Thing']
module = modules[__name__]
for name, value in chain(events.items(), things.items()):
    setattr(module, name, value)
    __all__.append(name)

from creatures import Male, Female

if __name__ == '__main__':
    print dir()

