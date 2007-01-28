
import re
from decimal import Decimal
from cixar.python.xml.tags import tags, Tag, Name
from cixar.python.iterkit import any, chain
from cixar.python.wrap import wrap
from cixar.python.text import uncomment, blocks

class Layer(Tag):

    def __init__(self, label = None):
        self.name = 'g'
        self.label = label
        self.gs = []

    def append(self, g):
        self.gs.append(g)

    @property
    def elements(self):
        return []

    @property
    def attributes(self):
        return {}

class Svg(Layer):

    def __init__(self, width = None, height = None, size = None):
        if width is None or height is None:
            assert width is None and height is None
            assert size is not None
            width, height = size
        self.name = 'svg'
        self.width = width
        self.height = height
        self.defs = {}
        self.gs = []

    @property
    def elements(self):
        return (
            [
                tags.defs(
                    definition
                    for definition in self.defs.values()
                ),
            ] +
            self.gs
        )

    @property
    def attributes(self):
        return {
            'height': self.height,
            'width': self.width,
            'xmlns': 'http://www.w3.org/2000/svg',
            'xmlns:svg': 'http://www.w3.org/2000/svg',
            'xmlns:xlink': 'http://www.w3.org/1999/xlink',
            'xmlns:inkscape': 'http://www.inkscape.org/namespaces/inkscape',
            'xmlns:dc': 'http://purl.org/dc/elements/1.1/',
            'xmlns:cc': 'http://web.resource.org/cc/',
            'xmlns:rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
            'xmlns:sodipodi': 'http://inkscape.sourceforge.net/DTD/sodipodi-0.dtd',
            'version': 1.0,
        }

class Rectangle(Tag):
    def __init__(
        self,
        x = None,
        y = None,
        height = None,
        width = None,
        rx = None,
        ry = None,
        start = None,
        stop = None,
        size = None,
        round = None,
        **attributes
    ):
        self.name = 'rect'
        if x is None or y is None:
            assert start is not None
            x, y = start
        if width is None or height is None:
            if size is None:
                assert stop is not None
                x1, y1 = stop
                size = x1 - x, y1 - y
            width, height = size
        if round is not None:
            rx, ry = round
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rx = rx
        self.ry = ry
        self._attributes = attributes

    @property
    def start(self):
        return self.x, self.y

    @property
    def stop(self):
        return self.x + self.width, self.y + self.height

    @property
    def size(self):
        return self.width, self.height

    @property
    def attributes(self):
        self._attributes.update({
            'x': '%spx' % self.x,
            'y': '%spx' % self.y,
            'width': '%spx' % self.width,
            'height': '%spx' % self.height,
            'rx': '%spx' % self.rx,
            'ry': '%spx' % self.ry,
        })
        return self._attributes

    @property
    def elements(self):
        return []

def parse(file):
    return Tag.parse(file)

def label_iter(image):
    for child in image:
        if (
            isinstance(child, Tag) and
            child.name == 'g' and
            'inkscape:label' in child
        ):
            yield child['inkscape:label']

labels = wrap(list)(label_iter)

def label_layer_iter(image):
    for child in image:
        if (
            isinstance(child, Tag) and
            child.name == 'g' and
            'inkscape:label' in child
        ):
            yield (child['inkscape:label'], child)

label_layer = wrap(dict)(label_layer_iter)

def topo_sorted_iter(items, lt_table):

    visited = set()

    def inner_topo_sorted(key, inner_visited = None):

        if inner_visited is None:
            inner_visited = set()

        if key in inner_visited:
            raise Exception("cycle")

        visited.add(key)
        inner_visited.add(key)

        for inner in lt_table[key]:
            if inner in visited:
                continue
            for item in inner_topo_sorted(inner, inner_visited):
                yield item

        yield key

    for key in items:
        if key not in visited:
            for line in inner_topo_sorted(key):
                yield line

topo_sorted = wrap(list)(topo_sorted_iter)

class Rules(dict):

    def __getitem__(self, key):
        if key not in self:
            self[key] = set() 
        return super(Rules, self).__getitem__(key)

def parse_rules(labels, rules_files):

    edges = tuple(
        chain(*[
            blocks(uncomment(rules_file))
            for rules_file in rules_files
        ])
    )

    labels = set(labels)
    for row in edges:
        for expression in row:
            if re.match(r'^[\w\d_]+$', expression):
                labels.add(expression)

    # table of nodes to nodes that are less than that node
    lt_table = Rules()

    for row in edges: 

        equivalences = []
        for expression in row:
            matchers = tuple(
                re.compile('^%s$' % part)
                for part in expression.split(' ')
            )
            matches = tuple(
                label
                for label in labels
                if any(
                    matcher.match(label)
                    for matcher in matchers
                )
            )
            if not matches:
                #print 'no labels match the expression', `expression`
                pass
            equivalences.append(matches)

        for index in range(1, len(equivalences)):
            lessers = equivalences[index - 1]
            greaters = equivalences[index]
            for lesser in lessers:
                for greater in greaters:
                    lt_table[greater].add(lesser)

    return lt_table

