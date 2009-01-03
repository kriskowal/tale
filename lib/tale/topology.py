
class index_property(object):
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

    y, x, size = (index_property(n) for n in range(3))

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
    def __get__(self, objekt, klass):
        while objekt.scope > 0:
            objekt = objekt.children[self.index]
        return objekt

class PlanarTree(NaryTree):

    edge_len = 1

    @property
    def children_len(self):
        return self.edge_len ** 2

    @property
    def size(self):
        return self.edge_len ** self.scope

    @property
    def child_size(self):
        return self.size / self.edge_len

    def __init__(self, scope = 0, x = 0, y = 0, parent = None, **kws):
        # deliberately bypasses the NaryTree initializer
        super(NaryTree, self).__init__(**kws)
        if scope is None:
            scope = self.scope
        self.scope = scope
        self.parent = parent
        self.box = Box((y, x, self.size))
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
                        parent = self,
                        scope = child_scope,
                        x = self.box.x + x * self.child_size,
                        y = self.box.y + y * self.child_size,
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

    def go(self, x = None, y = None, size = None, to = None, fro = None):

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
             return self.parent.go(to = to, fro = fro)

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

    north_west_quadrant = ChildProperty(0)
    north_east_quadrant = ChildProperty(1)
    south_west_quadrant = ChildProperty(2)
    south_east_quadrant = ChildProperty(3)
    north_west_corner = CornerProperty(0)
    north_east_corner = CornerProperty(1)
    south_west_corner = CornerProperty(2)
    south_east_corner = CornerProperty(3)

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
    from doctest import testmod
    testmod()

