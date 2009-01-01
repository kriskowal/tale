
from things import Thing, Unique
from people import Person
from creatures import Male, Female
from lrucache import LruCache

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
        self.it = None
        self.they = None
        self.he = None
        self.she = None
        self.names = {} # LruCache(7) # object to name
        self.objects = {} # LruCache(7) # name to object
        self.genders = {} # objects to their known genders
        self.names[self] = 'narrator'
        self.stuff = set() # stuff you 'own'
        # classes that the narrator knows and presumes their audience knows about too
        self.knowledge = {} # names of objects that the narrator presumes the audience knows them by
        self.vocabulary = set([Thing])

        self.sensitivity = 1
        self.olfactory_sensitivity = 1
        self.aural_sensitivity = 1
        self.visual_sensitivty = 1

    def narrate_story(self, story):
        pass

    def narrate_events(self, events):
        if events is None:
            return
        return '  '.join(
            story for story in (
                self.narrate_event(event)
                for event in events
            ) if story is not None
        )

    def narrate_event(self, event):
        if event.impact >= self.sensitivity:
            return self.narrate_(event.subject, event, event.object, *event.modifiers, **event.transitives)

    def narrate_(self, subject, verb, object = None, *modifiers, **transitives):
        parts = []
        parts.append(self.verb(subject, verb))
        parts.insert(0, self.noun(subject))
        if object is not None:
            parts.append(self.noun(object, subject))
        for modifier in modifiers:
            parts.append(modifier)
        for modifier, object in transitives.items():
            parts.append([modifier.lower(), self.noun(object)])
        return sentential(parts)

    def verb(self, subject, verb):
        if subject is self.they:
            return verb.personal_present
        if subject is self.audience or subject is self.narrator:
            return verb.personal_present
        return verb.present

    def noun(self, object, subject = None):

        if isinstance(object, basestring):
            return '"%s"' % object

        a = False
        the = False

        # recognize
        if object is self.narrator:
            if subject is object: name = 'myself'
            elif subject: name = 'me'
            else: name = 'I'
        elif object is self.audience:
            if subject is object: name = 'yourself'
            else: name = 'you'
        elif object is self.it:
            if subject is object: name = 'itself'
            else: name = 'it'
        elif object is self.they:
            if subject is object: name = 'themself'
            else: name = 'they'
        elif object is self.she:
            if object is subject: name = 'herself'
            elif subject: name = 'her'
            else: name = 'she'
        elif object is self.he:
            if object is subject: name = 'himself'
            elif subject: name = 'him'
            else: name ='he'
        elif object in self.names:
            name = self.names[object]
            the = True
        elif isinstance(object, Unique):
            name = object.singular
            the = True
        else:
            # describe
            # distinguish
            # generalize
            if getattr(object, 'name', None) is not None:
                name = object.name
            else:
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
                self.it = None
            else:
                self.it = object

        self.names[name] = object

        if a: name = ('a', name)
        elif the: name = ('the', name)

        return name

from people import Person
class Narrator(Person):
    singular = 'narrator'

if __name__ == '__main__':

    from people import Person, Human
    from mammals import Cat
    from things import Hat
    from events import *

    you = Person(gender = Male)
    gwen = Person(gender = Female, name = "Gwen")
    narrator = Narrator()
    narrate = narrator.narrate(you)
    narrate = narrate.narrate_event
    cat = Cat()
    man = Human(gender = Male)
    hat = Hat()

    print narrate(Hit(you, narrator))
    print narrate(Hit(narrator, you))
    print narrate(Hit(you, you))
    print narrate(Hit(narrator, narrator))
    print narrate(Hit(you, narrator, 'again'))
    print narrate(Hit(you, narrator, 'again', With = 'predudice'))
    print narrate(Hit(you, cat))
    print narrate(Hit(cat, you))
    print narrate(Kick(man, cat))
    print narrate(Kick(you, man))
    print narrate(Kick(you, hat))
    print narrate(Kick(you, hat, 'again'))
    print narrate(Kill(cat, gwen))

