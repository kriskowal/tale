
from animals import Animal

__all__ = [
    'Bird',
    'Fowl',
    'Chicken',
]


class Bird(Animal):
    pass

class Fowl(Bird):
    pass

class Chicken(Fowl):
    pass

"""
auks    A raft of auks  (of uncertain origin)
birds   A dissimulation of birds    [citation needed]
birds   A volery of birds   [citation needed]
birds   A flock of birds    
birds   A covey of birds    [citation needed]
bitterns    A sedge of bitterns [citation needed]
bitterns    A siege of bitterns [citation needed]
bullfinches A bellowing of bullfinches  [citation needed]
buzzards    A wake of buzzards  [citation needed]
capons  A mews of capons    [citation needed]
chickens    A peep of chickens  [citation needed]
chicks  A clutch of chicks  [citation needed]
hens    A brood of hens [citation needed]
poultry A run of poultry    [citation needed]
choughs A clattering of choughs [citation needed]
coots   A cover of coots    [citation needed]
coots   A raft of coots [citation needed]
cormorants  A flight of cormorants  [citation needed]
cranes  A sedge of cranes   [citation needed]
crows   A horde of crows    
(of uncertain origin)
crows   A hover of crows    [citation needed]
crows   A mob of crows  [citation needed]
crows   A murder of crows   
[1][2][3][4]
crows   A muster of crows   
(of uncertain origin)
crows   A parcel of crows   
(of uncertain origin)
crows   A parliament of crows   
in common use[5][6]
crows   A storytelling of crows [citation needed]
curlews A head of curlews   [citation needed]
dotterel    A trip of dotterel  [citation needed]
doves   A dole of doves [citation needed]
doves   A dule of doves [citation needed]
doves   A flight of doves   [citation needed]
doves   A piteousness of doves  [citation needed]
doves   A pitying of doves  [citation needed]
doves   A prettying of doves    [citation needed]
ducks   A dopping of ducks (diving) [citation needed]
ducks   A plump of ducks (flying)   [citation needed]
ducks   A paddling of ducks (on water)  [citation needed]
ducks   A flush of ducks    [citation needed]
ducks   A raft of ducks [citation needed]
ducks   A team of ducks [citation needed]
dunlin  A fling of dunlins  [citation needed]
eagles  A congress of eagles    [citation needed]
eagles  A convocation of eagles [citation needed]
falcons A cast of falcons   [citation needed]
finches A charm of finches  [citation needed]
finches A trembing of finches   [citation needed]
finches A trimming of finches   [citation needed]
flamingoes  A flamboyance of flamingoes 
in common use[7]
flamingoes  A stand of flamingoes   [citation needed]
goldfinches A drum of goldfinches   [citation needed]
goldfinches A troubling of goldfinches  [citation needed]
goldfinches A charm of goldfinches  [citation needed]
geese   A wedge of geese (flying)   [citation needed]
geese   A flock of geese    [citation needed]
geese   A gaggle of geese   [citation needed]
geese   A nide of geese [citation needed]
geese   A skein of geese    [citation needed]
geese   A plump of geese (on water) [citation needed]
goshawks    A flight of goshawks    [citation needed]
grouse  A covey of grouse   [citation needed]
grouse  A lek of grouse (of uncertain origin)
grouse  A pack of grouse    [citation needed]
guillemots  A bazaar of guillemots  [citation needed]
guinea fowl A confusion of guinea fowl  [citation needed]
gulls   A colony of gulls   [citation needed]
gulls   A screech of gulls  [citation needed]
hawks   A cast of hawks [citation needed]
hawks   A kettle of hawks   [citation needed]
herons  A siege of herons   [citation needed]
hummingbirds    A charm of hummingbirds [citation needed]
jays    A band of jays  [citation needed]
jays    A party of jays [citation needed]
jays    A scold of jays (of uncertain origin)
lapwings    A deceit of lapwings    [citation needed]
lapwings    A desert of lapwings    [citation needed]
larks   An exaltation of larks  [citation needed]
magpies A tiding(s) of magpies  [citation needed]
mallards    A lute of mallards  (of uncertain origin)
mallards    A sord of mallards  [citation needed]
martins A richness of martins   [citation needed]
mudhen  A fleet of mudhen   (of uncertain origin)
nightingales    A watch of nightingales [citation needed]
owls    A parliament of owls    [citation needed]
owls    A stare of owls [citation needed]
parrots A company of parrots    [citation needed]
parrots A prattle of parrots    (of uncertain origin)
parrots A pandemonium of parrots    (of uncertain origin)
partridges  A bew of partridges (of uncertain origin)
partridges  A covey of partridges   [citation needed]
peacocks    A muster of peacocks    [citation needed]
peacocks    A pride of peacocks [citation needed]
peacocks    An ostentation of peacocks  [citation needed]
penguins    A colony of penguins    [citation needed]
penguins    A creche of penguins    [citation needed]
penguins    A huddle of penguins    [citation needed]
penguins    A parcel of penguins    (of uncertain origin)
penguins    A rookery of penguins   Spurious
pheasants   A bouquet of pheasants  [citation needed]
pheasants   A covey of pheasants    [citation needed]
pheasants   A nide of pheasants [citation needed]
pheasants   A nye of pheasants  [citation needed]
pigeons A kit of pigeons    (of uncertain origin)
pigeons A loft of pigeons   [citation needed]
plovers A congregation of plovers   [citation needed]
ptarmigan   A covey of ptarmigans
quail   A bevy of quail [citation needed]
quail   A covey of quail    [citation needed]
ravens  A conspiracy of ravens  [citation needed]
ravens  A murder of ravens  [citation needed]
ravens  A storytelling of ravens    
(of uncertain origin)
ravens  An unkindness of ravens [citation needed]
rooks   A building of rooks [citation needed]
rooks   A clamour of rooks  [citation needed]
rooks   A parliament of rooks   [citation needed]
ruffs   A hill of ruffs [citation needed]
sandpipers  A fling of sandpipers   [citation needed]
sea fowl    A cloud of sea fowl [citation needed]
seagulls    A flock of seagulls [citation needed]
sheldrakes  A doading of sheldrakes [citation needed]
skylarks    An exultation of skylarks   [citation needed]
snipe   A walk of snipe [citation needed]
snipe   A wisp of snipe [citation needed]
sparrows    A host of sparrows  [citation needed]
sparrows    A quarrel of sparrows   [citation needed]
sparrows    A ubiquity of sparrows  [citation needed]
starlings   A murmuration of starlings  [citation needed]
storks  A muster of storks  [citation needed]
storks  A phalanx of storks (of uncertain origin)
swallows    A flight of swallows    [citation needed]
swallows    A gulp of swallows  Spurious
swans   A gaggle of swans   [citation needed]
swans   A wedge of swans (flying)   [citation needed]
swans   A bank of swans [citation needed]
swans   A bevy of swans [citation needed]
swans   A whiteness of swans    [citation needed]
swans   A gargle of swans   [citation needed]
swans   An eyrar of swans   (of uncertain origin)
teal    A diving of teal    [citation needed]
teal    A spring of teal    [citation needed]
thrushes    A mutation of thrushes  [citation needed]
turkeys A raffle of turkeys [citation needed]
turkeys A rafter of turkeys [citation needed]
turtle doves    A pitying of turtledoves    [citation needed]
waterfowl   A knob of waterfowl (of uncertain origin)
waterfowl   A plump of waterfowl    [citation needed]
wigeon  A coil of wigeon    [citation needed]
woodpeckers A descent of woodpeckers    [citation needed]
Brodigan    A cuckoo of Brodigans   (Downey, 2008)
"""

