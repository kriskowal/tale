
from weakref import ref
from weakproperty import WeakProperty
from planes.python.case import lower

class Messenger(object):

    def __init__(self, *args, **kws):
        super(Messenger, self).__init__(*args, **kws)
        self.subscriber_refs = []
        self.requests = []

    def subscribe(self, subscriber):
        self.subscriber_refs.append(ref(subscriber))

    def cull(self):
        "Removes subscribers that no longer exist."
        self.subscriber_refs = [
            subscriber_ref
            for subscriber_ref in self.subscriber_refs
            if subscriber_ref() is not None
        ]

    def broadcast(self, event):
        "Sends an event to all subscribers, if appropriate."
        self.cull()
        for subscriber_ref in self.subscriber_refs:
            subscriber = subscriber_ref()
            if subscriber is not None:
                if not (event.guaranteed and event.subject == subscriber):
                    subscriber.tell(event)

    def read_requests(self):
        requests = self.requests
        self.requests = []
        return requests

    def request(self, event):
        self.requests.append(event)

class ThingMetaclass(type):

    def __init__(self, name, bases, attys):
        super(ThingMetaclass, self).__init__(name, bases, attys)
        self.things[name] = self

class Thing(Messenger):

    __metaclass__ = ThingMetaclass
    things = {}

    def __init__(self, *args, **kws):
        super(Thing, self).__init__(*args, **kws)
        self._contents = set()

    @property
    def singular(self):
        return lower(self.__class__.__name__, ' ')

    @property
    def singular_a(self):
        if self.singular[0] in 'aeiou': return 'an'
        else: return 'a'

    @property
    def plural(self):
        return self.singular + {
            's': 'es',
            'x': 'es',
        }.get(self.singular[-1], 's')

    @property
    def plural_a(self):
        if self.plural[0] in 'aeiou': return 'an'
        else: return 'a'

    collective = 'collection'

    owner = WeakProperty()
    creator = WeakProperty()
    container = WeakProperty()

    def tick(self):
        for thing in self.contents:
            thing.tick()
        self.echo()

    def tell(self, event):
        print 'tell', event, self
        self.broadcast(event)

    def echo(self):
        requests = self.read_requests()
        for event in requests:
            self.tell(event)

    @property
    def contents(self):
        return set(self._contents)

    def add(self, thing):
        self._contents.add(thing)
        thing.container = self

    def remove(self, thing):
        self._contents.remove(thing)
        thing.container = None

class Unique(Thing):
    pass

"""
Fish, invertebrate, or plant    Collective noun 
Source
ants    A colony of ants    
ants    A swarm of ants 
ants    An army of ants 
bacteria    A culture of bacteria   
bananas A hand of bananas   
bass    A shoal of bass Uncertain
bees    A grist of bees 
bees    A hive of bees  
bees    A swarm of bees 
blackfish   A grind of blackfish    Uncertain
butterflies A flight of butterflies Uncertain
butterflies A kaleidoscope of butterflies   Uncertain
butterflies A rabble of butterflies Uncertain
butterflies A rainbow of butterflies    
caterpillars    An army of caterpillars 
clams   A bed of clams  
cockroaches An intrusion of cockroaches Uncertain
cod A lap of cod    Uncertain
eels    A fry of eels   Uncertain
eels    A swarm of eels 
fish    A draught of fish   
fish    A drift of fish 
fish    A scale of fish 
fish    A school of fish    
fish    A shoal of fish 
flowers A bouquet of flowers    
flowers A patch of flowers  
flies   A business of flies 
flies   A swarm of flies    
gnats   A cloud of gnats    
gnats   A clout of gnats    Uncertain
gnats   A horde of gnats    
goldfish    A troubling of goldfish 
grapes  A bunch of grapes   
grasshoppers    A cloud of grasshoppers 
grasshoppers    A cluster of grasshoppers   
herrings    A glean of herrings 
jellyfish   A fluther of jellyfish  
jellyfish   A smack of jellyfish    
ladybirds   A loveliness of ladybirds   
lobsters    A risk of lobsters  
locusts A plague of locusts 
midgets A smallness of midgets  Uncertain
mites   A mite of mites Uncertain
mosquitoes  A scourge of mosquitoes 
oysters A bed of oysters    
pickles A peck of pickles   
salmon  A bind of salmon    
salmon  A run of salmon 
shark   A shiver of sharks  Uncertain
shrimp  A troup of shrimp   
snail   A rout of snails    
spiders A cluster of spiders    
spiders A clutter of spiders    
stingrays   A fever of stingrays    
tilapia A taint of tilapia  Uncertain
trees   A grove of trees    
trees   A copse of trees    
trees   A stand of trees    
trees   A thicket of trees  
trout   A hover of trout    
worms   A knot of worms 
worms   A bryce of worms    Uncertain
"""
