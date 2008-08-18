
from cixar.tale.svg import Svg, Rectangle, Decimal
from cixar.tale.svg.fill import Region, fill
from cixar.python.xml.tags import tags, Tag, Name
from cixar.python.iterkit import first
from random import randint
import re

def get_size(box):
    return tuple(Decimal(n) for n in (box['width'], box['height']))
def get_start(box):
    return tuple(Decimal(n) for n in (box['x'], box['y']))

mushrooms = Svg.parse(file('art/terrain/tree-poplar.svg'))
layers = mushrooms.layers

unit = get_size(first(layers['unit'].tags))
scale = 500, 500

sizes = {}

for label, layer in mushrooms.layers.items():
    if re.match(r'^\d+$', label):

        crop, path = (
            first(
                element
                for element in layers['%s-%s' % (label, suffix)].elements 
                if isinstance(element, Tag)
            )
            for suffix in ('crop', 'path')
        )

        crop_size, path_size = (
            get_size(box)
            for box in (crop, path)
        )
        crop_size, path_size = (
            (width / unit[0] * scale[0], height / unit[1] * scale[1])
            for width, height in (crop_size, path_size)
        )

        x, y = crop_start = get_start(path)
        clip = layer.translated(x = -x, y = -y).scaled(scale[0] / unit[0])

        sizes[path_size] = clip

svg = Svg(size = (1000, 1000))

print sizes

regions = sorted(fill([Region(start = (250, 250), size = (500, 500))], sizes.keys()))

for region in regions:
    start = region.start
    size = region.size
    clip = sizes[size]
    svg.append(clip.translated(start))

svg.writexml(file('temp.svg', 'w'))

