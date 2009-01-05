
class IndexProperty(object):
    def __init__(self, index):
        self.index = index
    def __get__(self, instance, klass):
        return instance[self.index]
    def __set__(self, instance, value):
        instance[self.index] = value

class Box(tuple):
    """

        provides a convenience interface for two
        dimensional coordinate tuples or boxes.
        Boxes are triples that include the size of
        the box at a given coordinate.

        The Box class provides properties for accessing
        indicies by the names 'y', 'x', and 'size'.  The
        class also provides a __contains__ method so that
        you can check whether a box geometrically
        contains another.

    """

    y, x, size = (IndexProperty(n) for n in range(3))

    def __contains__(self, other):
        """
            Notes whether this coordinate box
            completely subcontains an other box.

            >>> big = Box((0, 0, 4))
            >>> small = Box((1, 1, 2))
            >>> outside = Box((2, 2, 3))

            +-----------+ big
            |           |
            |  +-----+ small
            |  |     |  |
            |  |  +--|--|--+ outside
            |  |  |  |  |  |
            |  +-----+  |  |
            |     |     |  |
            +-----------+  |
                  |        |
                  +--------+

            >>> assert small in big
            >>> assert big not in small
            >>> assert outside not in big
            >>> assert big not in outside

            Also, boxes that consume
            all of another box's area, or
            are inside but on an outer
            edge are still "inside".

            >>> assert big in big
            >>> assert small in small

        """
        y, x, size = self
        iy, ix, isize = other
        return (
            isize <= size and
            x <= ix and
            ix + isize <= x + size and
            y <= iy and
            iy + isize <= y + size
        )

class Direction(int):
    names = (
        'north',
        'south',
        'west',
        'east',
    )
    def __str__(self):
        return self.names[self]

directions = n, s, w, e = (
    north,
    south,
    west,
    east
) = tuple(
    Direction(index) for index in range(4)
)

class Quadrant(int):
    names = (
        'north_west',
        'north_east',
        'south_west',
        'south_east',
    )
    def __str__(self):
        return self.names[self]

quadrants = nw, ne, sw, se = (
    north_west,
    north_east,
    south_west,
    south_east 
) = tuple(
    Quadrant(index) for index in range(4)
)

class ChildProperty(object):
    def __init__(self, index):
        self.index = index
    def __get__(self, objekt, klass):
        return objekt.children[self.index]
    def __set__(self, objekt, child):
        objekt.children[self.index] = child

class NaryTree(object):

    children_len = 0
    scope = 0

    @property
    def Child(self):
        return type(self)

    @property
    def Children(self):
        return [
            self.Child
            for n in range(self.children_len)
        ]

    def get_child_type(self, n):
        if hasattr(self.Children[n], '__get__'):
            return self.Children[n].__get__(self, self.__class__)
        return self.Children[n]

    def __init__(self, scope = None, parent = None, **kws):
        super(NaryTree, self).__init__(**kws)
        if not hasattr(self, 'Children'):
            self.Children = tuple(
                self.Child
                for n in range(self.children_len)
            )
        if scope is None:
            scope = self.scope
        self.scope = scope
        self.parent = parent
        if scope > 0:
            child_scope = scope - 1
            self.children = [
                self.get_child_type(n)(
                    scope = child_scope,
                    parent = self
                )
                for n in range(self.children_len)
            ]

    def __iter__(self):
        return iter(self.children)

    def __getitem__(self, n):
        return self.children[n]

    @property
    def top_to_bottom(self):
        """
        Produces an iteration of all nodes starting at the
        root and ending with every leaf.
        """
        yield self
        if self.scope:
            for child in self.children:
                for node in child.top_to_bottom:
                    yield node

    @property
    def bottom_to_top(self):
        """
        Produces an iteration of all nodes starting with the
        leaves and wending back to the root.
        """
        if self.scope:
            for child in self.children:
                for node in child.bottom_to_top:
                    yield node
        yield self

    @property
    def top_down(self):
        """
        Produces an iteration of all nodes, starting with the
        root, but omitting all of the leaves.  This traversal is good
        for visiting each node and pushing data down one level since
        it never visits the floor.
        """
        yield self
        if self.scope > 1:
            for child in self.children:
                for node in child.top_down:
                    yield node

    @property
    def bottom_up(self):
        """
        Produces an iteration of all nodes, starting with the leaves
        on the floor and traveling upward toward the root but never
        visiting the root.  This traversal is good for visiting
        each node of the tree and pushing data up one level since it
        never visits the root.
        """
        if self.scope:
            for child in self.children:
                for node in child.bottom_up:
                    yield node
        if self.parent:
            yield self

class CornerProperty(object):
    def __init__(self, index):
        self.index = index
    def __get__(self, plane, Plane):
        while plane.scope > 0:
            plane = plane.children[plane.corner_indicies[self.index]]
        return plane

class Edge(object):
    def __init__(self, plane, axis, bias):
        self.plane = plane
        self.axis = axis
        self.bias = bias
    def __getitem__(self, n):
        if isinstance(n, slice):
            start = n.start
            stop = n.stop
            step = n.step
            if start is None: start = 0
            if start < 0: start += self.plane.size
            if stop is None: stop = self.plane.size
            if stop < 0: stop += self.plane.size
            if step is None: step = 1
            return [self[n] for n in range(start, stop)][::step]
        else:
            if n < 0:
                n = n + self.plane.size
            a, b = n, (self.plane.size - 1) * self.bias
            if self.axis == 'x': x, y = a, b
            if self.axis == 'y': y, x = a, b
            return self.plane.go(to = Box((self.plane.y + y, self.plane.x + x, 1)))

class EdgeProperty(object):
    def __init__(self, axis, bias):
        self.axis = axis
        self.bias = bias
    def __get__(self, plane, Plane):
        return Edge(plane, self.axis, self.bias)

class PlanarTree(NaryTree):

    edge_len = 1

    north_west_corner = CornerProperty(north_west)
    north_east_corner = CornerProperty(north_east)
    south_west_corner = CornerProperty(south_west)
    south_east_corner = CornerProperty(south_east)
    north_edge = EdgeProperty('x', 0)
    south_edge = EdgeProperty('x', 1)
    west_edge = EdgeProperty('y', 0)
    east_edge = EdgeProperty('y', 1)

    @property
    def north(self):
        return self.go(x = 0, y = -1)

    @property
    def south(self):
        return self.go(x = 0, y = 1)

    @property
    def west(self):
        return self.go(x = -1, y = 0)
        
    @property
    def east(self):
        return self.go(x = 1, y = 0)
        
    @property
    def box(self):
        return Box((self.y, self.x, self.size))

    @property
    def corner_indicies(self):
        return [
            0,
            self.edge_len - 1,
            self.edge_len ** 2 - self.edge_len,
            self.edge_len ** 2 - 1,
        ]

    def __init__(
        self,
        scope = None,
        y = 0,
        x = 0,
        parent = None,
        root = None,
        **kws
    ):
        # deliberately bypasses the NaryTree initializer
        super(NaryTree, self).__init__(**kws)
        if root is None:
            root = self
        if scope is None:
            scope = self.scope
        self.scope = scope
        self.root = root
        self.parent = parent
        self.y = y
        self.x = x
        if scope > 0:
            child_scope = scope - 1
            child_types = [
                self.get_child_type(n)
                for n in range(self.children_len)
            ]
            child_types = iter(child_types)
            self.plane = [
                [
                    child_types.next()(
                        y = self.box.y + y * self.child_size,
                        x = self.box.x + x * self.child_size,
                        scope = child_scope,
                        parent = self,
                        root = root,
                    )
                    for x in range(self.edge_len)
                ]
                for y in range(self.edge_len)
            ]
            self.children = [
                self.plane[y][x]
                for y in range(self.edge_len)
                for x in range(self.edge_len)
            ]

    def __contains__(self, other):
        if hasattr(other, 'root') and self.root is other.root:
            return other.box in self.box
        while other:
            if other is self:
                return True
            other = other.parent

    @property
    def children_len(self):
        return self.edge_len ** 2

    @property
    def size(self):
        return self.edge_len ** self.scope

    @property
    def child_size(self):
        return self.size / self.edge_len

    def to(self, x = None, y = None, size = None):
        if size is None: size = 1
        if x is None: x = 0
        if y is None: y = 0
        to = Box((x, y, size))
        return self.go(to = to)

    def go(self, x = None, y = None, size = None, to = None, fro = None, **kws):

        fro = self.box

        if size is None:
            size = 0
        if to is None:
            to = Box((fro.y + y, fro.x + x, fro.size + size))

        if to == fro:
            return self
        elif to in self.box:
            return self.plane[
                (to.y - fro.y) / self.child_size
            ][
                (to.x - fro.x) / self.child_size
            ].go(to = to, fro = fro)
        elif self.parent is None:
            return
        else:
            return self.parent.go(to = to, fro = fro, fro_node = self)

class QuadTree(PlanarTree):
    """\

        >>> q = QuadTree(scope = 1)
        >>> q.south_west_corner.box
        (1, 0, 1)
        >>> q.south_west_corner == q.plane[1][0]
        True
        >>> q.south_west_corner.north == q.north_west_corner
        True
        >>> q.south_west_corner.east == q.south_east_corner
        True
        >>> q.south_east_corner.south == None
        True

    """

    edge_len = 2

    corner_indicies = range(4)

    north_west_quadrant = ChildProperty(north_west)
    north_east_quadrant = ChildProperty(north_east)
    south_west_quadrant = ChildProperty(south_west)
    south_east_quadrant = ChildProperty(south_east)

    @property
    def center(self):
        return self.north_west_quadrant.south_east_corner

    def __repr__(self):
        return '<%s %d,%d %d>' % (
            self.__class__.__name__,
            self.box.x,
            self.box.y,
            self.box.size,
        )

class Scaffold(object):
    def __init__(self, node, *args, **kws):
        super(Scaffold, self).__init__(*args, **kws)
        self.node = node
        if node.scope:
            self.children = [
                self.__class__(child)
                for child in node.children
            ]
        self.do()
    def do(self):
        return

if __name__ == '__main__':

    class OrderedTests(tuple):
        def items(self): return self

    __test__ = OrderedTests((
        ('degenerate_directions', '''\
            >>> q = QuadTree(scope = 0)
            >>> q
            <QuadTree 0,0 1>
            >>> q.north
            >>> q.south
            >>> q.east
            >>> q.west
        '''),
        ('degenerate_corners', '''
            >>> q = QuadTree(scope = 0)
            >>> q.north_east_corner == q
            True
            >>> q.north_west_corner == q
            True
            >>> q.south_east_corner == q
            True
            >>> q.south_west_corner == q
            True
        '''),
        ('x', '''
            >>> q = QuadTree(scope = 2)
            >>> q.north_edge[:]
            [<QuadTree 0,0 1>, <QuadTree 1,0 1>, <QuadTree 2,0 1>, <QuadTree 3,0 1>]
            >>> q.north_edge[::2]
            [<QuadTree 0,0 1>, <QuadTree 2,0 1>]
            >>> q.north_edge[::-1]
            [<QuadTree 3,0 1>, <QuadTree 2,0 1>, <QuadTree 1,0 1>, <QuadTree 0,0 1>]
        '''),
    ))

    from doctest import testmod
    testmod()

