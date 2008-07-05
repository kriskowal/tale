
class Event(object):

    impact = 1
    aural = 0
    visual = 0
    olfactory = 0
    thermal = 0
    mystical = 0

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

    @property
    def present(self):
        return self.personal_present + 's'

    @property
    def personal_present(self):
        return self.__class__.__name__.lower()

    @property
    def past(self):
        return self.present + 'ed'

    @property
    def past_perfect(self):
        return self.past

    def tick(self, context):
        pass

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

