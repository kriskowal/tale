
height = 5

class Tile(Quadtree):
    def __init__(self, height = 5):
        super(Tile, self).__init__(height = 5)

class Face(object):
    def __init__(self):
        self.tiles = list(
            list(
                Tile(y, x)
                for x in range(2)
            )
            for y in range(3)
        )

class Cube(object):
    def __init__(self):
        self.faces = list(
            Face(n) for n in range(6)
        )

