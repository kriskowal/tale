__all__ = [
    'Event',
    'Say',
    'Hit',
    'Kick',
    'Kill',
]

class Event(object):

    @property
    def present(self):
        return self.personal_present + 's'

    @property
    def personal_present(self):
        return self.__class__.__name__.lower()

    @property
    def past(self):
        return self.present + 'ed'

    def __init__(self, subject, object = None, *modifiers, **transitives):
        self.subject = subject
        self.object = object
        self.transitives = transitives
        self.modifiers = modifiers

class Say(Event):
    past = 'said'

class Hit(Event):
    pass

class Kick(Event):
    pass

class Kill(Event):
    pass

