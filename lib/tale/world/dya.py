
from tale.topology import QuadTree, PlanarTree, NaryTree, ChildProperty, CornerProperty, Box
from tale.world.things import Thing

class Roomy(object):
    @property
    def rooms(self):
        if self.scope:
            for child in self.children:
                for room in child.rooms:
                    yield room
        else:
            yield self

class Face(PlanarTree, Roomy, Thing):
    edge_len = 3
    child_size = 2

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
            return Node(face = self, **kws)
        return Child

    def __repr__(self):
        return '<%s %dx%d>' % (
            self.__class__.__name__,
            self.box.size,
            self.box.size,
        )

class Node(QuadTree, Roomy):
    def __init__(self, face, **kws):
        self.face = face
        super(Node, self).__init__(**kws)

    def get_child_type(self, n):
        def Child(**kws):
            if self.scope > 1:
                return Node(face = self.face, **kws)
            else:
                return Room(face = self.face, **kws)
        return Child

    def __repr__(self):
        return '<%s %d,%d %dx%d>' % (
            self.face.__class__.__name__,
            self.box.x,
            self.box.y,
            self.box.size,
            self.box.size,
        )

class Room(Node, Thing):

    def add(self, objekt):
        pass

    def __repr__(self):
        return '<%s %d,%d>' % (
            self.face.__class__.__name__,
            self.box.x,
            self.box.y,
        )

class FaceProperty(object):
    def __init__(self, name):
        self.name = name
    def __get__(self, objekt, klass):
        return getattr(objekt.parent, self.name)

class Dysia(Face):
    number = 1
    order = 6
    dychotomy = 3
    trychotomy = 0
    philosophy = 'dyalectics'
    tone = 'c'
    color = 'magenta'
    north = FaceProperty('borea')
    south = FaceProperty('austra')
    west = FaceProperty('occia')
    east = FaceProperty('oria')

    def specify(self, z, y, x):
        return z, y
    def generalize(self, y, x):
        return y, self.size - 1 - x, self.size - 1

class Oria(Face):
    number = 2
    order = 5
    dychotomy = 2
    trychotomy = 0
    philosophy = 'dyocease'
    tone = 'c#'
    color = 'yellow'
    north = FaceProperty('borea')
    south = FaceProperty('austra')
    west = FaceProperty('dysia')
    east = FaceProperty('euia')

    def specify(self, z, y, x):
        return z, self.size - 1 - x
    def generalize(self, y, x):
        return y, self.size - 1, self.size - 1 - x

class Austra(Face):
    number = 3
    order = 4
    dychotomy = 1
    trychotomy = 0
    philosophy = 'dyocease'
    tone = 'e'
    color = 'cyan'
    north = FaceProperty('oria')
    south = FaceProperty('occia')
    west = FaceProperty('dysia')
    east = FaceProperty('euia')

    def specify(self, z, y, x):
        return self.size - 1 - y, self.size - 1 - x
    def generalize(self, y, x):
        return self.size - 1, y, self.size - 1 - x

class Borea(Face):
    number = 4
    order = 3
    dychotomy = 1
    trychotomy = 1
    philosophy = 'dyanetics'
    tone = 'a#'
    color = 'red'
    north = FaceProperty('oria')
    south = FaceProperty('occia')
    west = FaceProperty('euia')
    east = FaceProperty('dysia')

    def specify(self, z, y, x):
        return self.size - 1 - y, x
    def generalize(self, y, x):
        return 0, self.size - 1 - y, x

class Occia(Face):
    number = 5
    order = 2
    dychotomy = 2
    trychotomy = 1
    philosophy = 'dyalectics'
    tone = 'g'
    color = 'blue'
    north = FaceProperty('borea')
    south = FaceProperty('austra')
    west = FaceProperty('euia')
    east = FaceProperty('dysia')

    def specify(self, z, y, x):
        return z, x
    def generalize(self, y, x):
        return y, 0, x

class Euia(Face):
    number = 6
    order = 1
    dychotomy = 3
    trychotomy = 1
    philosophy = 'dyanetics'
    tone = 'f#'
    color = 'green'
    north = FaceProperty('borea')
    south = FaceProperty('austra')
    west = FaceProperty('oria')
    east = FaceProperty('occia')

    def specify(self, z, y, x):
        return z, self.size - 1 - y
    def generalize(self, y, x):
        return y, self.size - 1 - x, 0

class Dya(NaryTree, Roomy, Thing):
    children_len = 6

    scope = 3
    assert scope >= 3, 'dya scope must be at least three to support underlying objects.'

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
        child_size = 3 * 2 ** (self.scope - 2)
        return '<%s 6x%dx%d>' % (
            self.__class__.__name__,
            child_size,
            child_size,
        )

    def go(self, to = None, fro = None, fro_node = None, **kws):
        if to[0] < 0: direction = 'north'
        elif to[0] >= fro_node.size: direction = 'south'
        elif to[1] < 0: direction = 'west'
        else: direction = 'east'
        to_node = getattr(fro_node, direction)
        y, x = to_node.specify(*fro_node.generalize(to[0], to[1]))
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

    ))

    from doctest import testmod
    testmod()

