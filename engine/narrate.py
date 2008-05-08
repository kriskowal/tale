
from things import Thing
from creatures import Male, Female

__all__ = [
    'Narrator',
]

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

class Narration(object):

    def __init__(self, narrator, audience):
        self.narrator = narrator
        self.audience = audience
        self.it = None
        self.he = None
        self.she = None
        self.names = {} # object to name
        self.objects = {} # name to object
        self.names[self] = 'narrator'
        self.stuff = set() # stuff you 'own'
        # classes that the narrator knows and presumes their audience knows about too
        self.knowledge = {} # names of objects that the narrator presumes the audience knows them by
        self.vocabulary = set([Thing])

    def narrate_story(self, story):
        pass

    def narrate_event(self, event):
        return self.narrate_(event.subject, event, event.object, *event.modifiers, **event.transitives)

    def narrate_(self, subject, verb, object = None, *modifiers, **transitives):
        parts = []
        parts.append(self.noun(subject))
        parts.append(self.verb(subject, verb))
        if object is not None:
            parts.append(self.noun(object, subject))
        for modifier in modifiers:
            parts.append(modifier)
        for modifier, object in transitives.items():
            parts.append([modifier.lower(), object])
        return sentential(parts)

    def verb(self, subject, verb):
        if subject is self.audience or subject is self.narrator:
            return verb.personal_present
        return verb.present

    def noun(self, object, subject = None):

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
        elif object is self.she:
            if object is subject: name = 'herself'
            elif subject: name = 'her'
            else: name = 'she'
        elif object is self.he:
            if object is subject: name = 'himself'
            elif subject: name = 'him'
            else: name ='he'
        elif object in self.names:
            print 'recalled'
            name = self.names[object]
            the = True
        else:
            # describe
            # distinguish
            # generalize
            if hasattr(object, 'name'):
                name = object.name
            else:
                name = object.singular
                a = True

        # learn
        if object is not self.audience:
            if hasattr(object, 'gender'):
                if object.gender == Male:
                    self.he = object
                if object.gender == Female:
                    self.she = object
            else:
                self.it = object
        self.names[name] = object

        if a: name = ('a', name)
        if the: name = ('the', name)
        return name

from people import Person
class Narrator(Person):
    singular = 'narrator'

if __name__ == '__main__':

    you = Player(gender = Male)
    gwen = Player(gender = Female, name = "Gwen")
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

