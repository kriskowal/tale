
from itertools import chain
from tale.topology import QuadTree, PlanarTree, NaryTree, ChildProperty, CornerProperty, Box
from tale.world.things import Thing

WORLD_SCOPE = 5

class Room(Thing):
    """
    A baseclass for all room-like objects, those that
    are or contain rooms, whose contents include their
    tree children.
    """

    @property
    def contents(self):
        return chain(
            getattr(self, 'children', ()),
            super(Room, self).contents,
        )

    @property
    def container(self):
        return self.parent

    @property
    def rooms(self):
        if self.scope:
            for child in self.children:
                for room in child.rooms:
                    yield room
        else:
            yield self

class Tile(QuadTree, Room):
    """
    A base class for the pips and tiles of a die, and all rooms
    therein.
    """
    def __init__(self, face, **kws):
        self.face = face
        super(Tile, self).__init__(**kws)

    def get_child_type(self, n):
        def Child(**kws):
            return self.__class__(face = self.face, **kws)
        return Child

    def __repr__(self):
        if self.scope > 1:
            return '<%s %d,%d %dx%d>' % (
                self.face.__class__.__name__,
                self.box.x,
                self.box.y,
                self.box.size,
                self.box.size,
            )
        else:
            return '<%s %d,%d>' % (
                self.face.__class__.__name__,
                self.box.x,
                self.box.y,
            )

class SeaTile(Tile): pass
class MountainTile(Tile): pass
class IceMountainTile(Tile): pass
class VolcanoTile(Tile): pass
class DysTile(Tile): pass
class PlainsTile(Tile): pass
class IcePlainsTile(Tile): pass
class DesertTile(Tile): pass
class MushroomForestTile(Tile): pass

class Face(PlanarTree, Room):
    scope = WORLD_SCOPE - 1
    edge_len = 3
    child_size = 2 ** (WORLD_SCOPE - 2)

    (
        north_west_pip,
        north_pip,
        north_east_pip,
        west_pip,
        center_pip,
        east_pip,
        south_west_pip,
        south_pip,
        south_east_pip,
    ) = (ChildProperty(n) for n in range(edge_len ** 2))

    @property
    def center(self):
        return self.plane[1][1].center

    @property
    def size(self):
        return self.edge_len * 2 ** (self.scope - 1)

    def get_child_type(self, n):
        def Child(**kws):
            Tile = self.Tiles[self.pips[n % 3][n / 3]]
            return Tile(face = self, **kws)
        return Child

    def __repr__(self):
        return '<%s %dx%d>' % (
            self.__class__.__name__,
            self.box.size,
            self.box.size,
        )

class FaceProperty(object):
    def __init__(self, name):
        self.name = name
    def __get__(self, objekt, klass):
        return getattr(objekt.parent, self.name)

class Euia(Face):
    number = 6
    order = 1
    dychotomy = 3
    trychotomy = 1
    philosophy = 'dyanetics'
    tone = 'f#'
    color = 'green'
    Tiles = (PlainsTile, MountainTile)
    pips = (
        (1, 1, 1),
        (0, 0, 0),
        (1, 1, 1),
    )

    north = FaceProperty('borea')
    south = FaceProperty('austra')
    west = FaceProperty('oria')
    east = FaceProperty('occia')

    def specify(self, z, y, x):
        return z, self.size - 1 - y
    def generalize(self, y, x):
        return y, self.size - 1 - x, 0

class Occia(Face):
    number = 5
    order = 2
    dychotomy = 2
    trychotomy = 1
    philosophy = 'dyalectics'
    tone = 'g'
    color = 'blue'
    Tiles = (SeaTile, MushroomForestTile)
    pips = (
        (1, 0, 1),
        (0, 1, 0),
        (1, 0, 1),
    )

    north = FaceProperty('borea')
    south = FaceProperty('austra')
    west = FaceProperty('euia')
    east = FaceProperty('dysia')

    def specify(self, z, y, x):
        return z, x
    def generalize(self, y, x):
        return y, 0, x

class Borea(Face):
    number = 4
    order = 3
    dychotomy = 1
    trychotomy = 1
    philosophy = 'dyanetics'
    tone = 'a#'
    color = 'red'
    Tiles = (IcePlainsTile, IceMountainTile)
    pips = (
        (1, 0, 1),
        (0, 0, 0),
        (1, 0, 1),
    )

    north = FaceProperty('oria')
    south = FaceProperty('occia')
    west = FaceProperty('euia')
    east = FaceProperty('dysia')

    def specify(self, z, y, x):
        return self.size - 1 - y, x
    def generalize(self, y, x):
        return 0, self.size - 1 - y, x

class Austra(Face):
    number = 3
    order = 4
    dychotomy = 1
    trychotomy = 0
    philosophy = 'dyocease'
    tone = 'e'
    color = 'cyan'
    Tiles = (SeaTile, IceMountainTile)
    pips = (
        (0, 0, 1),
        (0, 1, 0),
        (1, 0, 0),
    )

    north = FaceProperty('oria')
    south = FaceProperty('occia')
    west = FaceProperty('dysia')
    east = FaceProperty('euia')

    def specify(self, z, y, x):
        return self.size - 1 - y, self.size - 1 - x
    def generalize(self, y, x):
        return self.size - 1, y, self.size - 1 - x

class Oria(Face):
    number = 2
    order = 5
    dychotomy = 2
    trychotomy = 0
    philosophy = 'dyocease'
    tone = 'c#'
    color = 'yellow'
    Tiles = (DesertTile, VolcanoTile)
    pips = (
        (1, 0, 0),
        (0, 0, 0),
        (0, 0, 1),
    )

    north = FaceProperty('borea')
    south = FaceProperty('austra')
    west = FaceProperty('dysia')
    east = FaceProperty('euia')

    def specify(self, z, y, x):
        return z, self.size - 1 - x
    def generalize(self, y, x):
        return y, self.size - 1, self.size - 1 - x

class Dysia(Face):
    number = 1
    order = 6
    dychotomy = 3
    trychotomy = 0
    philosophy = 'dyalectics'
    tone = 'c'
    color = 'magenta'
    Tiles = (DesertTile, DysTile)
    pips = (
        (0, 0, 0),
        (0, 1, 0),
        (0, 0, 0),
    )

    north = FaceProperty('borea')
    south = FaceProperty('austra')
    west = FaceProperty('occia')
    east = FaceProperty('oria')

    def specify(self, z, y, x):
        return z, y
    def generalize(self, y, x):
        return y, self.size - 1 - x, self.size - 1

class Dya(NaryTree, Room):
    """
    The root of the world-tree, the entire six sided die.
    """

    scope = Face.scope + 1
    child_size = 3 * 2 ** (scope - 2)
    children_len = 6

    def __init__(self, *args, **kws):
        super(Dya, self).__init__(*args, **kws)

    Children = (Dysia, Oria, Austra, Borea, Occia, Euia)
    dysia, oria, austra, borea, occia, euia = (
        ChildProperty(n)
        for n in range(6)
    )

    @property
    def faces(self):
        return self.children

    def __contains__(self, room):
        return True

    def __repr__(self):
        return '<%s 6x%dx%d>' % (
            self.__class__.__name__,
            self.child_size,
            self.child_size,
        )

    def go(self, to = None, fro = None, fro_node = None, **kws):
        if to.y < 0:
            direction = 'north'
        elif to.y >= fro_node.size:
            direction = 'south'
        elif to.x < 0:
            direction = 'west'
        elif to.x >= fro_node.size:
            direction = 'east'
        to_node = getattr(fro_node, direction)
        y, x = to_node.specify(*fro_node.generalize(*to[:2]))
        to = Box((y, x, to.size))
        return to_node.go(to = to)

if __name__ == '__main__':

    dya = Dya()

    class OrderedTests(tuple):
        def items(self): return self

    __test__ = OrderedTests((
        ('containment', """
            >>> dya.dysia is dya[1 - 1]
            True
            >>> dya.euia is dya[6 - 1]
            True
            >>> dya.euia.center in dya.euia
            True
            >>> dya.euia in dya
            True
            >>> dya in dya.euia
            False
            >>> dya.euia in dya.dysia
            False
            >>> dya.euia.center in dya.dysia.center
            False
        """),

        ('corners', '''
            >>> def north_west_corner(room):
            ...    while hasattr(room, 'children'):
            ...        room = room.children[0]
            ...    return room
            ...
            >>> dya.euia.north_west_corner == north_west_corner(dya.euia)
            True
        '''),

        ('grouping', """
            >>> sorted(dya.faces, key = lambda face: (face.dychotomy, face.trychotomy)) == [dya.austra, dya.borea, dya.oria, dya.occia, dya.dysia, dya.euia]
            True
        """),

        ('travel', '''
            >>> at = dya.euia.center
            >>> at.north.south == at
            True
            >>> at.south.north == at
            True
            >>> at.west.east == at
            True
            >>> at.east.west == at
            True
        '''),

        ('edges', '''
            >>> at = dya.euia
            >>> at.north_edge[0] == at.north_west_corner
            True
            >>> at.north_edge[1] == at.north_west_corner.east
            True
            >>> at.north_edge[-1] == at.north_east_corner
            True
            >>> at.south_edge[0] == at.south_west_corner
            True
            >>> at.south_edge[-1] == at.south_east_corner
            True
            >>> at.west_edge[0] == at.north_west_corner
            True
            >>> at.west_edge[-1] == at.south_west_corner
            True
            >>> at.east_edge[0] == at.north_east_corner
            True
            >>> at.east_edge[-1] == at.south_east_corner
            True
        '''),

        ('face_directions', '''
            >>> dya.euia.north == dya.borea
            True
            >>> dya.euia.east.east.east.east == dya.euia
            True
            >>> dya.occia.north.north.south.south == dya.occia
            True
        '''),

        ('edge_travel', '''
            >>> dya.borea.specify(*dya.euia.generalize(0, 0)) == (0, 0)
            True
            >>> dya.euia.north_west_corner.north == dya.borea.north_west_corner
            True
            >>> dya.euia.north_east_corner.north == dya.borea.south_west_corner
            True
            >>> dya.euia.north_west_corner.west ==  dya.oria.north_east_corner
            True
            >>> dya.euia.south_west_corner.west ==  dya.oria.south_east_corner
            True
            >>> dya.euia.south_west_corner.south == dya.austra.north_east_corner
            True
            >>> dya.euia.south_east_corner.south == dya.austra.south_east_corner
            True
        '''),

        ('tick_propagation', '''
            >>> dya = Dya()
            >>> class Foo(Thing):
            ...     def tick(self):
            ...         super(Foo, self).tick()
            ...         print 'foo tick'
            ...
            >>> dya.euia.center.add(Foo())
            >>> dya.tick()
            foo tick
        '''),
        
        ('container_attribute', '''
            >>> def ultimate(thing):
            ...     while thing.container is not None:
            ...         thing = thing.container
            ...     return thing
            ...
            >>> dya = Dya()
            >>> thing = Thing()
            >>> dya.euia.center.add(thing)
            >>> ultimate(thing) == dya
            True
        '''),

        ('tile_types', '''
            >>> dya.euia.center.__class__.__name__
            'PlainsTile'
            >>> dya.dysia.center.__class__.__name__
            'DysTile'
            >>> dya.oria.north_west_corner.__class__.__name__
            'VolcanoTile'
        '''),

    ))

    from doctest import testmod
    testmod()

