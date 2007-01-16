
from cixar.python.xml.tags import tags, Tag
from cixar.python.wrap import wrap

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

