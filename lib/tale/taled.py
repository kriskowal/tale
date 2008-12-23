
from weakref import ref
from itertools import count
import simplejson
from xml.sax.saxutils import escape

from planes.lazy import\
    PathService,\
    FileTreeService,\
    FileService,\
    Response,\
    SessionService,\
    JsonService,\
    JsonRequestService,\
    JsonResponseService,\
    FunctionService
from planes.python.mix import mix
from planes.python.module_path import module_path
from planes.python.mode import Modal, Mode

import tale

class CommandSession(PathService):

    def __init__(self):

        self.messages = []
        self.requests = []
        self.new_session = True

        def command_service(request):
            self.command(request.path[1:])
            request.finish()

        @JsonRequestService
        def command_json_service(request, object):
            self.requests.insert(0, request)
            self.requests[2:] = []
            if request.session_lost:
                self.new_session = True
            self.command(object['command'])
            self.flush()

        def push_service(request):
            self.requests.insert(0, request)
            self.requests[2:] = []
            if request.session_lost:
                self.new_session = True
            self.flush()

        super(CommandSession, self).__init__(
            paths = {
                'command': command_service,
                'command.json': command_json_service,
                'push.json': push_service,
            },
        )

    def get_messages(self):
        response = {
            'newSession': self.new_session,
            'messages': [
                {
                    'html': escape(self.messages[n]),
                }
                for n in range(0, len(self.messages))
            ],
        }
        self.messages[:] = []
        self.new_session = False
        return response

    def flush(self):
        if self.requests and (self.messages or self.new_session):
            request = self.requests.pop(0)
            response = self.get_messages()
            request.output.write(simplejson.dumps(response))
            request.finish()

    def output(self, message):
        self.messages.append(message)
        self.flush()

    def command(self, command):
        pass

from engine.narrate import Narrator, Narrative
from engine.events import Say

from engine.events import Kick
import engine.people as engine_people

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
        self.session.output(self.narrative.narrate_event(event))
    def command(self, command):
        self.player.command(command)

class ModalCommandSession(Modal, CommandSession):
    def __init__(self, engine, *args, **kws):
        self.engine = engine
        super(ModalCommandSession, self).__init__(*args, **kws)
    def Mode(self):
        return Mode(self)
    def command(self, command):
        self.mode.command(command)

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
        self.players.append(ref(player))
        return player
    def tick(self):
        self.players = [player_ref for player_ref in self.players if player_ref() is not None]
        requests = self.read_requests()
        for player_ref in self.players:
            player = player_ref()
            for event in requests:
                player.signal(event)
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

from engine.events import Say

class Player(Observable, engine_people.Person):
    def __init__(self, engine, *args, **kws):
        self.engine_ref = ref(engine)
        self.commands = []
        super(Player, self).__init__(*args, **kws)
    def command(self, command):
        self.commands.append(command)
    def read_commands(self):
        commands = self.commands
        self.commands = []
        return commands
    def tick(self):
        for command in self.read_commands():
            self.engine_ref().request(Say(self, command))

Engine = mix(TaleEngine, ReactorEngine)

def taled():

    from planes.lazy import\
        serve,\
        PathService,\
        AdhocKitService,\
        LogService,\
        ResponseService

    engine = Engine()
    service = TaleService(engine)
    service = PathService(paths = {'session': service})
    service = AdhocKitService(service)
    #service = LogService(service)
    service = ResponseService(service)
    serve(service, port = 2380, debug = True, engine = engine)

