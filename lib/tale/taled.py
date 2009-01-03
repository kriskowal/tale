
from weakref import proxy
from itertools import count
from xml.sax.saxutils import escape

from planes.lazy import\
    PathService,\
    Response,\
    SessionService,\
    JsonService,\
    JsonRequestService,\
    JsonResponseService,\
    FunctionService,\
    JsonConnectionService

from planes.python.mix import mix
from planes.python.module_path import module_path
from planes.python.mode import Modal, Mode

from tale.narrate import Narrator, Narrative
from tale.engine import Say, Kick, Person

class Mode(Mode):
    next_id = count().next
    def __init__(self, session, *args, **kws):
        self.id = self.next_id()
        self.session = session
        self.engine = session.engine
        self.player = self.engine.player()
        self.narrator = Narrator()
        self.narrative = Narrative(self.narrator, self.player)
        self.player.observe(self.observer)
        super(Mode, self).__init__(*args, **kws)
    def observer(self, event):
        print 'sent', event
        self.session.send({'html': escape(event)})
    def receive(self, command):
        print 'received', command
        self.player.command(command)

class ModalCommandSession(Modal, JsonConnectionService):
    def __init__(self, engine, *args, **kws):
        self.engine = engine
        super(ModalCommandSession, self).__init__(*args, **kws)
    def Mode(self):
        return Mode(self)
    def receive(self, command):
        self.mode.receive(command)

def TaleService(engine):
    def Session():
        return ModalCommandSession(engine)
    session_service = SessionService(Session)
    return session_service

class ReactorEngine(object):
    quantum = 1
    def __call__(self, reactor):
        def tick():
            self.tick()
            reactor.callLater(self.quantum, tick)
        tick()

class TaleEngine(object):
    def __init__(self, *args, **kws):
        self.players = []
        self.requests = []
        super(TaleEngine, self).__init__(*args, **kws)
    def player(self):
        player = Player(self)
        self.players.append(proxy(player, self.logouter(player)))
        return player
    def logouter(self, player):
        def logout():
            self.players.remove(player)
        return logout
    def tick(self):
        requests = self.read_requests()
        for player in self.players:
            for event in requests:
                if not (
                    event.guaranteed and
                    event.subject == player
                ):
                    player.tell(event)
            player.tick()
    def read_requests(self):
        requests = self.requests
        self.requests = []
        return requests
    def request(self, event):
        self.requests.append(event)

class Observable(object):
    def __init__(self, *args, **kws):
        self.observers = []
        super(Observable, self).__init__(*args, **kws)
    def observe(self, observer):
        self.observers.append(observer)
    def signal(self, event):
        for observer in self.observers:
            observer(event)

class Player(Observable, Person):
    def __init__(self, location, *args, **kws):
        self.location = location
        self.commands = []
        self.narrator = Narrator()
        self.narrate = Narrative(self.narrator, self)
        super(Player, self).__init__(*args, **kws)
    def command(self, command):
        self.commands.append(command)
    def tell(self, event):
        self.signal(self.narrate(event))
    def read_commands(self):
        commands = self.commands
        self.commands = []
        return commands
    def tick(self):
        for command in self.read_commands():
            event = Say(self, command)
            if event.guaranteed:
                self.tell(event)
            self.location.request(Say(self, command))

Engine = mix(TaleEngine, ReactorEngine)

def taled():

    from planes.lazy import\
        serve,\
        PathService,\
        ResponseService

    engine = Engine()
    service = TaleService(engine)
    service = PathService(paths = {'session': service})
    service = ResponseService(service)
    serve(service, port = 2380, debug = True, engine = engine)

