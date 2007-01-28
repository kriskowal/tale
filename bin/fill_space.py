
from random import randint, choice
from cixar.tale.svg import Svg, Rectangle, Decimal
from cixar.python.color import DisonanceSpectrum
disonance_spectrum = iter(DisonanceSpectrum())

class Region(Rectangle):

    def __init__(self, *arguments, **keywords):
        super(Region, self).__init__(*arguments, **keywords)
        self._attributes['opacity'] = '.25'
        self._attributes['fill'] = '#%s' % str(disonance_spectrum.next())

    def overlaps(self, other):
        (Ax0, Ay0), (Ax1, Ay1) = other.start, other.stop
        (Bx0, By0), (Bx1, By1) = self.start, self.stop
        left = (Bx0 > Ax0 and Bx0 < Ax1) or (Ax0 > Bx0 and Ax0 < Bx1)
        right = (Bx1 < Ax1 and Bx1 > Ax0) or (Ax1 < Bx1 and Ax1 > Bx0)
        top = (By0 > Ay0 and By0 < Ay1) or (Ay0 > By0 and Ay0 < By1)
        bottom = (By1 < Ay1 and By1 > Ay0) or (Ay1 < By1 and Ay1 > By0)
        return (left or right) and (top or bottom)

    def bust_iter(self, other):
        (Ax0, Ay0), (Ax1, Ay1) = other.start, other.stop
        (Bx0, By0), (Bx1, By1) = self.start, self.stop
        left = (Ax0 <= Bx0 and Bx0 < Ax1) or (Bx0 <= Ax0 and Ax0 < Bx1)
        right = (Bx1 <= Ax1 and Ax0 < Bx1) or (Ax1 <= Bx1 and Bx0 < Ax1)
        top = (Ay0 <= By0 and By0 < Ay1) or (By0 <= Ay0 and Ay0 < By1)
        bottom = (By1 <= Ay1 and Ay0 < By1) or (Ay1 <= By1 and By0 < Ay1)
        count = 0
        
        # left
        if left and (top or bottom):
            yield Region(
                start = (Ax0, Ay0),
                stop = (Bx0, Ay1),
            )
            count += 1

        # right
        if right and (top or bottom):
            yield Region(
                start = (Bx1, Ay0),
                stop = (Ax1, Ay1),
            )
            count += 1

        # top
        if top and (left or right):
            yield Region(
                start = (Ax0, Ay0),
                stop = (Ax1, By0),
            )
            count += 1

        # bottom
        if bottom and (left or right):
            yield Region(
                start = (Ax0, By1),
                stop = (Ax1, Ay1),
            )
            count += 1

        if not count: 
            yield other

    def bust(self, other):
        return list(self.bust_iter(other))

    def busts_iter(self, others):
        for other in others:
            for bust in self.bust(other):
                yield bust

    def busts(self, others):
        return list(self.busts_iter(others))

    def __repr__(self):
        return 'Region(%s, %s)' % (self.start, self.stop)

def fill(svg, regions, sizes):

    min_width = min(width for width, height in sizes)
    min_height = min(height for width, height in sizes)

    area = sum(region.height * region.width for region in regions)

    while regions:

        width, height = size = choice(sizes)
        region = choice(regions)

        if width > region.width or height > region.height:
            continue

        rectangle = Region(
            start = (
                region.x + randint(0, region.width - width),
                region.y + randint(0, region.height - height),
            ),
            size = size
        )
        svg.append(rectangle)

        area -= rectangle.height * rectangle.width
        assert area > 0, 'More area has been consumed than exists in the fillable regions'

        regions = rectangle.busts(regions)
        regions = [r for r in regions if r.width >= min_width and r.height >= min_height]

size = 1000, 1000
svg = Svg(size = size)
try:
    fill(svg, [Region(start = (0, 0), stop = size)], [(100, 100), (100, 50), (50, 50)])
except AssertionError, error:
    print 'assertion error', error
svg.writexml(file('temp.svg', 'w'))

