__all__ = [
    'Thing',
    'Hat',
    'Quote',
    'Claim',
]

class Thing(object):
    @property
    def singular(self):
        return self.__class__.__name__.lower()
    @property
    def plural(self):
        return self.singular + 's'
    collective = 'collection'

class Hat(Thing):
    pass


# things that can be said

class Quote(Thing):
    def __init__(self, sentence):
        self.sentence = sentence

class Claim(Thing):
    def __init__(self, sentence):
        self.sentence = sentence

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
