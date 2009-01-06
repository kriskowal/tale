
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
from tale.world import Person, Dya
from tale.commands import do, chat

class Mode(Mode):
    next_id = count().next
    def __init__(self, session, *args, **kws):
        self.id = self.next_id()
        self.session = proxy(session)
        self.player = session.engine.player()
        self.player.observe(self.observer)
        super(Mode, self).__init__(*args, **kws)
        self.session.send({'html': 'Welcome to Dya.  Try <tt>/help</tt> for details.'})
    def observer(self, event):
        self.session.send({'html': escape(event)})
    def receive(self, command):
        chat(self, command)

class ModalCommandSession(JsonConnectionService, Modal):
    def __init__(self, engine, *args, **kws):
        self.engine = engine
        super(ModalCommandSession, self).__init__(*args, **kws)
    def Mode(self):
        return Mode(self)
    def receive(self, message):
        self.mode.receive(message)

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
        self.world = Dya()
        self.players = []
        super(TaleEngine, self).__init__(*args, **kws)
    def player(self):
        player = Player(self.world.euia.center)
        self.players.append(proxy(player, self.logouter(player)))
        return player
    def logouter(self, player):
        def logout():
            self.players.remove(player)
        return logout
    def tick(self):
        self.world.tick()
        for player in self.players:
            player.tick()

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
        self.requests = []
        self.narrator = Narrator()
        self.narrative = Narrative(self.narrator, self)
        location.subscribe(self)
        super(Player, self).__init__(*args, **kws)
    def request(self, request):
        self.requests.append(request)
    def read_requests(self):
        requests = self.requests
        self.requests = []
        return requests
    def tell(self, event):
        self.signal(self.narrative(event))
    def tick(self):
        for event in self.read_requests():
            if event.guaranteed:
                self.tell(event)
            self.location.request(event)

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

