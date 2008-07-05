
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
        x, y, size = self
        ix, iy, isize = other
        return (
            isize <= size and
            x <= ix and
            ix < x + size and
            y <= iy and
            iy < y + size
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

class Corners(object):
    def __init__(self, node):
        self.node = node
    nw = north_west = property(lambda self: self.node.corner(nw))
    ne = north_east = property(lambda self: self.node.corner(ne))
    sw = north_west = property(lambda self: self.node.corner(sw))
    se = north_west = property(lambda self: self.node.corner(se))

def is_power_of_two(n):
    # This is a highly optimized way to check whether
    #  an integer is a power of two.  In binary, any power
    #  of two has only one bit turned on.  Any number
    #  that's one less than a power of two is therefore
    #  a bit mask for all of the bits that are less
    #  significant than the high bit from the power
    #  of two.  The bitwise negation of
    #  that bitmask displays all of the bits of greater
    #  or equal significance to that bit.  Additionally
    #  this bit mask is guaranteed to display only the
    #  high order bits of /any/ number.  Only a power
    #  of two is equal to the bitwise and of itself
    #  and it's corresponding mask of higher order bits.
    return n == n & ~(n - 1)

def is_power_of_four(n):
    # This is a highly optimized way to check whether
    #  an integer is a power of four.  A power of four
    #  has the same constraint of having only one
    #  bit turned on, but has the additional constraint
    #  that only every other bit represents a power of
    #  four.  By performing a bitwise and of the
    #  given number with a mask of all of the elligible
    #  bits (...0101 == 0x...5), we can ascertain this
    #  latter constraint.
    return power_of_two(n) and n & 0x55555555 != 0

class Compound(object):

    children_len = 0

    @property
    def Child(self):
        return type(self)

    def __init__(self, height = 0):
        if height > 0:
            self.size = 2 ** height
            child_height = height - 1
            self.children = list(
                self.Child(child_height)
                for n in range(self.children_len)
            )

    def __html_repr__(self, kit):
        return

class Quadtree(object):

    children_len = 4

    def __init__(self, height = 0):
        super(Quadtree, self).__init__(height)

