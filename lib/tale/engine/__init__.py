"""
Herein lie things.
"""

#from events import *
#from things import *
#from people import *
#!ls *.py | cut -d. -f1
#
#aliens
#animals
#birds
#creatures
#events
#fish
#flowers
#insects
#invertebrates
#mammals
#people
#philosophers
#plants
#reptiles
#things
#trees

__all__ = []

# Import all classes from this directory
import os
mypath = os.path.dirname(__file__)
print 'mypath', mypath
sub_modules = [
    x[:-3] 
    for x in os.listdir(mypath or '.')
    if x[-2:] == 'py'
]
print 'sub_modules', sub_modules

for module in sub_modules:
    full_name = os.path.join(os.path.basename(mypath) + '.' + module)
    if module != '__init__':
        print 'loading', full_name
        #m = __import__(full_name)
        m = __import__(module, globals(), locals(), ['*'])
        print 'module:', m
        #__all__.append(m.__name__)
        print m.__name__

print __all__
if __name__ == '__main__':
    print dir()

