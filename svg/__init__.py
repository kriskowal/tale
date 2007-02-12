
import re
from decimal import Decimal
from cixar.python.xml.tags import tags, Tag, Name
from cixar.python.iterkit import any, chain
from cixar.python.wrap import wrap
from cixar.python.text import uncomment, blocks

class Layer(Tag):

    def __init__(
        self,
        label = None,
        groups = None,
        group = None,
        defs = None,
        attributes = None,
    ):
        if groups is None: groups = []
        if group is not None: groups.append(group)
        if defs is None: defs = {}
        if attributes is None: attributes = {}
        self.name = 'g'
        self.label = label
        self.groups = groups
        self.defs = defs
        self._attributes = attributes

    def append(self, group):
        if isinstance(group, Layer):
            self.defs.update(group.defs)
        self.groups.append(group)

    def translated(self, start = None, x = None, y = None, label = None):
        if x is None or y is None:
            assert x is None and y is None
            assert start is not None
            x, y = start
        if label is None: label = self.label
        return Layer(
            groups = [
                tags.g(
                    self.groups,
                    transform = 'translate(%s, %s)' % (x, y)
                )
            ],
            defs = self.defs,
            label = label
        )

    def scaled(self, factor, label = None):
        return Layer(
            groups = [
                tags.g(
                    self.groups,
                    transform = 'scale(%s)' % factor
                ),
            ],
            defs = self.defs,
            label = label,
        )

    @property
    def elements(self):
        return self.groups

    @property
    def attributes(self):
        attributes = self._attributes
        if self.label is not None:
            attributes['inkscape:label'] = self.label
        return attributes

class Svg(Layer):

    def __init__(
        self,
        width = None,
        height = None, 
        size = None,
        groups = None,
        group = None,
        defs = None,
    ):

        if width is None or height is None:
            assert width is None and height is None
            assert size is not None
            width, height = size
        if groups is None:
            groups = []
        if group is not None:
            groups.append(group)
        if defs is None:
            defs = {}

        self.name = 'svg'
        self.width = width
        self.height = height
        self.defs = defs
        self.groups = groups

    @property
    def elements(self):
        return (
            [
                tags.defs(
                    definition
                    for definition in self.defs.values()
                ),
            ] +
            self.groups
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

    @classmethod
    def parse(Self, file):
        xml = Tag.parse(file)
        return Self(
            width = xml['width'],
            height = xml['height'],
            groups = list(
                element
                for element in xml.tags
                if element.name == 'g'
            ),
            defs = dict(
                (element['id'], element)
                for element in xml[Name('defs')].tags
            ),
        )

    def label_iter(image):
        for element in image.tags:
            if (
                element.name == 'g' and
                'inkscape:label' in element
            ):
                yield element['inkscape:label']

    labels = property(wrap(list)(label_iter))

    def layers_iter(image):
        for child in image:
            if (
                isinstance(child, Tag) and
                child.name == 'g' and
                'inkscape:label' in child
            ):
                label = child['inkscape:label']
                yield label, Layer(
                    label,
                    groups = child.elements,
                    attributes = child.attributes
                )

    layers = property(wrap(dict)(layers_iter))

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

