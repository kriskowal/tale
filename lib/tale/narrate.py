
from engine import Event, Thing, Unique, Person, Male, Female, Creature
from planes.python.case import lower
from lrucache import LruCache

ordinals = [
    'first',
    'second',
    'third',
    'fourth',
    'fifth',
    'sixth',
    'seventh',
]

ordinal_suffixes = ['st', 'nd', 'rd', 'th']
def ordinal(n):
    if n / 10 % 10 == 1: return 'th'
    return ordinal_suffixes[min(3, (n + 9) % 10)]

def sentential(terms, within = None):
    def head(terms):
        if isinstance(terms, basestring):
            if len(terms) > 0: return terms[0].upper() + terms[1:]
            else: return ''
        else:
            if len(terms) > 0: return head(terms[0]) + ' ' + tail(terms[1:])
            else: return ''
    def tail(terms):
        return " ".join(
            isinstance(term, basestring) and term or tail(term)
            for term in terms
        )
    return head(terms) + '.'

def observe_gender(audience, object):
    if hasattr(object, 'show_gender'):
        shown_gender = object.show_gender(audience)
        if hasattr(audience, 'observe_gender'):
            observed_gender = audience.observe_gender(object)
            if observed_gender == shown_gender:
                return observed_gender

class Narrative(object):

    def __init__(self, narrator, audience):
        self.narrator = narrator
        self.audience = audience
        self.flush()

    def flush(self):
        self.it = None
        self.they = None # third person pronoun? plural third person pronoun?
        self.he = None
        self.she = None
        self.things = {'narrator': self} # the narrator
        self.others = {} # other things, if they've been displaced from primacy in things
        self.encounters = {} # encountered things in order by name
        self.names = {} # LruCache(7) # object to name
        self.objects = {} # LruCache(7) # name to object
        self.genders = {} # objects to their known genders

    def meet(self, person):
        self.names[person] = person.name
        self.he = None
        self.she = None
        self.they = None

    def knows(self, person):
        return isinstance(person, Person) and person in self.names

    def lookup(self, name):
        thing = None
        if name == 'him': thing = self.he
        if name == 'her': thing =  self.she
        if name == 'it': thing = self.it
        if name == 'them': thing = self.they
        if name in self.things: thing = self.things[name]
        self.noun(thing)
        return thing

    def __call__(self, story):
        if story is None:
            return
        elif isinstance(story, Event):
            return self.event(story)
        else:
            return self.events(story)

    def events(self, events):
        if events is None:
            return
        return '  '.join(
            story for story in (
                self.event(event)
                for event in events
            ) if story is not None
        )

    def event(self, event):
        return self.event_(event.subject, event, event.object, *event.modifiers, **event.transitives)

    def event_(self, subject, verb, object = None, *modifiers, **transitives):
        parts = []
        parts.append(self.verb(subject, verb))
        parts.insert(0, self.noun(subject))
        if object is not None:
            parts.append(self.noun(object, subject))
        for modifier in modifiers:
            parts.append(modifier)
        for modifier, object in transitives.items():
            parts.append([lower(modifier, ' '), self.noun(object, subject)])
        return sentential(parts)

    def verb(self, subject, verb):
        if (
            subject is self.audience or
            subject is self.narrator or
            subject is self.they
        ):
            return verb.personal_present # You say, I say, they say, (we say)
        return verb.present # He says, she says, it says, Joe says

    def noun(self, object, subject = None):

        if object is None:
            return 'nothing'

        if isinstance(object, basestring):
            return '"%s"' % object.replace('"', "'")

        a = False
        the = False
        other = False

        # recognize

        if object in self.names:
            name = self.names[object]
        elif object is self.narrator:
            if subject is object: name = 'myself'
            elif subject: name = 'me'
            else: name = 'I'
        elif object is self.audience:
            if subject is object: name = 'yourself'
            else: name = 'you'
        elif object is self.it:
            if subject is object: name = 'itself'
            else: name = 'it'
        elif object is self.she:
            if object is subject: name = 'herself'
            elif subject: name = 'her'
            else: name = 'she'
        elif object is self.he:
            if object is subject: name = 'himself'
            elif subject: name = 'him'
            else: name ='he'
        elif object is self.they:
            if subject is object: name = 'themself'
            elif subject: name = 'them'
            else: name = 'they'
        elif self.things.get(object.singular) == object:
            name = object.singular
            the = True
        elif self.others.get(object.singular) == object:
            name = object.singular
            the = True
            other = True
        elif object in self.encounters.get(object.singular, []):
            encounters = self.encounters[object.singular]
            name = (ordinals[encounters.index(object)], object.singular)
            the = True
        elif isinstance(object, Unique):
            name = object.singular
            the = True
        else:
            # describe
            # distinguish
            # generalize
            name = object.singular
            a = True

        # learn
        if object is not self.audience:
            if object in self.genders:
                gender = self.genders[object]
                if gender is Male:
                    self.he = object
                if gender is Female:
                    self.she = object
                self.it = None
            elif isinstance(object, Person):
                self.they = object
                self.he = None
                self.she = None
                self.it = None
            elif isinstance(object, Creature):
                self.it = None
            else:
                self.it = object

        encounters = self.encounters.setdefault(object.singular, [])
        if len(encounters) < len(ordinals) and object not in encounters:
            encounters.append(object)
        if self.others.get(object.singular) != self.things.get(object.singular):
            self.others[object.singular] = self.things.get(object.singular)
        self.things[object.singular] = object

        # add articles
        if a and name == 'person':
            name = 'someone'
        elif other:
            if a:
                name = ('another', name)
            elif the:
                name = ('the', 'other', name)
            else:
                name = ('some', 'other', name)
        elif a:
            name = (object.singular_a, name)
        elif the:
            name = ('the', name)

        return name

class Narrator(Person):
    singular = 'narrator'

if __name__ == '__main__':

    from engine import *

    you = Person(gender = Male)
    person1 = Person()
    person2 = Person()
    person3 = Person()
    gwen = Person(gender = Female, name = "Gwen")
    narrator = Narrator()
    cat = Cat()
    man = Human(gender = Male)
    Hat = type('Hat', (Thing,), {})
    hat = Hat()
    ash = AshTree()

    from doctest import testmod

    class __test__(object):
        @classmethod
        def items(self):
            return (
                (str(n), test)
                for n, test in enumerate((

                    """
                        >>> narrate = Narrative(narrator, you)
                        >>> narrate(Hit(you, narrator))
                        'You hit me.'
                        >>> narrate(Hit(narrator, you))
                        'I hit you.'
                        >>> narrate(Hit(you, you))
                        'You hit yourself.'
                        >>> narrate(Hit(narrator, narrator))
                        'I hit myself.'
                        >>> narrate(Hit(you, narrator, 'again'))
                        'You hit me again.'
                        >>> narrate(Hit(you, narrator, 'again', With = hat))
                        'You hit me again with a hat.'
                        >>> narrate(Hit(you, cat))
                        'You hit a cat.'
                        >>> narrate(Hit(cat, you))
                        'The cat hits you.'
                        >>> narrate(Kick(man, cat))
                        'A man kicks the cat.'
                        >>> narrate(Kick(you, man))
                        'You kick them.'
                        >>> narrate(Kick(you, hat))
                        'You kick the hat.'
                        >>> narrate(Kick(you, hat, 'again'))
                        'You kick it again.'
                        >>> narrate(Kill(cat, gwen))
                        'The cat kills someone.'
                        >>> narrate.meet(gwen)
                        >>> narrate(Kill(cat, gwen))
                        'The cat kills Gwen.'
                     """,

                     """
                        >>> narrate = Narrative(narrator, you)
                        >>> narrate(Say(person1, "Hi"))
                        'Someone says "Hi".'
                        >>> narrate(Say(person1, "Hi"))
                        'They say "Hi".'
                        >>> narrate(Say(you, "Hi", To = person1))
                        'You say "Hi" to them.'
                     """,

                     """
                        >>> narrate = Narrative(narrator, you)
                        >>> narrate(Say(person1, "Hi"))
                        'Someone says "Hi".'
                        >>> narrate(Say(gwen, "Hi"))
                        'Someone says "Hi".'
                        >>> narrate.meet(gwen)
                        >>> narrate(Say(gwen, "Hi"))
                        'Gwen says "Hi".'
                        >>> narrate(Say(person1, "Hi"))
                        'The other person says "Hi".'
                        >>> narrate(Say(person1, "Hi"))
                        'They say "Hi".'
                     """,

                     """
                        >>> narrate = Narrative(narrator, you)
                        >>> narrate(Say(person1, "Hi"))
                        'Someone says "Hi".'
                        >>> narrate(Say(person2, "Hi"))
                        'Someone says "Hi".'
                        >>> narrate(Say(person3, "Hi"))
                        'Someone says "Hi".'
                        >>> narrate(Say(gwen, "Hi"))
                        'Someone says "Hi".'
                        >>> narrate(Say(gwen, "Hi"))
                        'They say "Hi".'
                        >>> narrate(Say(person3, "Hi"))
                        'The other person says "Hi".'
                        >>> narrate(Say(person1, "Hi"))
                        'The first person says "Hi".'
                        >>> narrate(Say(person2, "Hi"))
                        'The second person says "Hi".'
                        >>> narrate(Say(person2, "Hi"))
                        'They say "Hi".'
                        >>> narrate(Say(person1, "Hi"))
                        'The first person says "Hi".'
                        >>> narrate(Say(person3, "Hi"))
                        'The third person says "Hi".'
                     """,

                     """
                        >>> narrate = Narrative(narrator, you)
                        >>> narrate(Fall(ash))
                        'An ash tree falls.'
                        >>> narrate.lookup('ash tree') is ash
                        True
                        >>> narrate.lookup('it') is ash
                        True
                        >>> narrate(Fall(hat))
                        'A hat falls.'
                        >>> narrate.lookup('ash tree') is ash
                        True
                        >>> narrate.lookup('it') is ash
                        True
                     """,

                     """
                        >>> narrate = Narrative(narrator, you)
                        >>> narrate.noun(None)
                        'nothing'
                     """,

                     r"""
                        >>> narrate = Narrative(narrator, you)
                        >>> narrate.noun('I said, "Hi!".')
                        '"I said, \'Hi!\'."'
                     """,

                     """
                        >>> narrate = Narrative(narrator, you)
                        >>> narrate(Say(person1, "Hi"))
                        'Someone says "Hi".'
                        >>> narrate(Say(person2, "Hi"))
                        'Someone says "Hi".'
                        >>> narrate(Say(person1, "Hi"))
                        'The other person says "Hi".'
                        >>> narrate(Say(person1, "Hi"))
                        'They say "Hi".'
                     """,

                 ))
            )

    testmod()

