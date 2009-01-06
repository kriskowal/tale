
from planes.python.case import lower

class EventMetaclass(type):
    """
        >>> Event.events_by_nominative['say'] == Say
        True
    """
    def __init__(self, name, bases, attys):
        super(EventMetaclass, self).__init__(name, bases, attys)
        lower_name = lower(name, ' ')
        self.nominative = attys.get('nominative', lower_name)
        self.present = attys.get('present', self.nominative + 's')
        self.past = attys.get('past', self.nominative + 'ed')
        self.past_perfect = attys.get('past_perfect', self.past)
        self.events[name] = self
        self.events_by_nominative[self.nominative] = self
        self.events_by_present[self.present] = self

class Event(object):

    __metaclass__ = EventMetaclass
    events = {}
    events_by_nominative = {}
    events_by_present = {}

    impact = 1
    aural = 0
    visual = 0
    olfactory = 0
    thermal = 0
    mystical = 0

    # denotes that the sender should see the event instantly, without
    #  having to wait for the engine to confirm and propagate.
    guaranteed = False

    def __init__(self, subject, object = None, *modifiers, **transitives):
        self.subject = subject
        self.object = object
        self.transitives = transitives
        self.modifiers = modifiers

    def impact(
        self,
        impact = None,
        visual = None,
        aural = None,
        olfactory = None,
        thermal = None,
        mystical = None,
    ):
        if impact is not None: self.impact = impact
        if aural is not None: self.aural = aural
        if visual is not None: self.visual = visual
        if olfactory is not None: self.olfactory = olfactory
        if thermal is not None: self.thermal = thermal
        if mystical is not None: self.mystical = mystical
        return self

    def tick(self, context):
        pass

    @classmethod
    def lookup(self, narrative, object):
        return narrative.lookup(object)

class Be(Event):
    present = 'is'
    past = 'was'
    past_perfect = 'been'

class Do(Event):
    present = 'does'
    past = 'did'
    past_perfect = 'done'
    
class Get(Event):
    past = 'got'
    past_perfect = 'gotten'

class Set(Event):
    past = 'set'

class Say(Event):
    past = 'said'
    guaranteed = True

    @classmethod
    def lookup(self, narrative, object):
        return object

class Hit(Event):
    past = 'hit'

class Kick(Event):
    pass

class Kill(Event):
    pass

class Tick(Event):
    pass

class Tock(Event):
    pass

class Attempt(Event):
    pass

class Appear(Event):
    pass

class Enter(Event):
    pass

class Exit(Event):
    pass

class Leave(Event):
    past = 'left'

class Laugh(Event):
    pass

class Lament(Event):
    pass

class Work(Event):
    pass

class Quaff(Event):
    pass

class Fall(Event):
    pass

class Solve(Event):
    past_perfect = 'solven'

class Explode(Event):
    def tick(self, context):
        yield Dematerialize(self.subject)

class Show(Event):
    past_perfect = 'shown'

class Materialize(Event):
    def tick(self, context):
        context.room.things.add(self.subject)

class Dematerialize(Event):
    impact = 0
    aural_impact = 0
    visual_impact = 0
    olfactory_impact = 0
    def tick(self, context):
        context.room.things.remove(self.subject)

class Remove(Event):
    def tick(self, context):
        self.subject.things.remove(self.object)

class Add(Event):
    def tick(self, context):
        self.subject.things.add(self.object)

class Move(Event):
    def tick(self, context):
        if self.subject.container is not None:
            yield Remove(self.subject.container, self.subject)
        self.subject.container = self.object
        yield Add(self.transitives['to'], self.subject)


if __name__ == '__main__':
    from doctest import testmod
    testmod()
