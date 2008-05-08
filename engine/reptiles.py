from animals import Animal

__all__ = [
    'Reptile',
    'Alligator',
    'Crocodile',
    'Lizard',
    'Iguana',
    'Monitor',
    'Snake',
    'Cobra',
    'Rattlesnake',
    'Viper',
    'Dragon',
    'Frog',
    'Toad',
    'Tortoise',
    'Turtle',
]


class Reptile(Animal):
    pass

class Alligator(Reptile):
    collective = 'congregation'

class Crocodile(Reptile):
    collective = 'bask' 
    #collective = 'congregation'
    #collective = 'float'
    #collective = 'nest'

class Lizard(Reptile):
    collective = 'lounge'

class Iguana(Lizard):
    collective = 'mess'

class Monitor(Lizard):
    collective = 'bank'

class Snake(Reptile):
    collective = 'slither'
    #collective = 'bed'
    #collective = 'den'
    #collective = 'nest'
    #collective = 'pit'

class Cobra(Snake):
    collective = 'quiver'

class Rattlesnake(Snake):
    collective = 'rhumba'

class Viper(Snake):
    #collective = 'nest'
    collective = 'den'

class Dragon(Snake, Lizard):
    collective = 'wing'
    #collective = 'flight'
    #collective = 'weyr'

class Frog(Reptile):
    collective = 'knot'
    #collective = 'army'
    #collective = 'colony'

class Toad(Reptile):
    collective = 'knob'
    #collective = 'knot'
    #collective = 'nest'
    #collective = 'lump'

class Tortoise(Reptile):
    collective = 'creep'

class Turtle(Reptile):
    collective = 'turn'
    #collective = 'bevy'
    #collective = 'bale'
    #collective = 'dule'
    #collective = 'nest'


"""
alligators  A congregation of alligators    
[1]
crocodiles  A bask of crocodiles    
[1]
crocodiles  A congregation of crocodiles    
[1]
crocodiles  A float of crocodiles   
[1]
crocodiles  A nest of crocodiles    
[1]
cobras  A quiver of cobras  
dragons A flight of dragons 
dragons A weyr of dragons   
dragons A wing of dragons   
frogs   An army of frogs    
[1]
frogs   A colony of frogs   
[1]
frogs   A knot of frogs 
[1]
iguanas A mess of iguanas   
[2]
lizards A lounge of lizards 
monitors    A bank of monitors  
rattlesnakes    A rhumba of rattlesnakes    
snakes  A bed of snakes 
[1]
snakes  A den of snakes 
[1]
snakes  A nest of snakes    
[1]
snakes  A pit of snakes 
[1]
snakes  A slither of snakes 
[1]
toads   A knot of toads 
[1]
toads   A nest of toads 
[1]
toads   A knob of toads 
[1]
toads   A lump of toads 
[1]
tortoises   A creep of tortoises    
[1]
turtles A bale of turtles   
[1]
turtles A bevy of turtles   
[1]
turtles A dule of turtles   
[1]
turtles A nest of turtles   
[1]
turtles A turn of turtles   
[1]
vipers  A nest of vipers    
[1]
vipers  A den of vipers 
[1]

"""
