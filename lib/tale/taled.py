
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

import simplejson

import tale
import planes.chiron
from planes.python.module_path import module_path
from xml.sax.saxutils import escape

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
        print 'flush', self.requests, self.messages, self.new_session
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

from planes.python.mode import Modal, Mode

class ModalCommandSession(Modal, CommandSession):

    def __init__(self, *args, **kws):
        super(ModalCommandSession, self).__init__(*args, **kws)

    def command(self, command):
        self.mode.command(command)

    class Mode(Mode):
        def command(self, command):
            self.modal.output(escape(command))

def TaleService():
    session_service = SessionService(ModalCommandSession)
    return session_service

def taled():

    from planes.lazy import\
        serve,\
        PathService,\
        AdhocKitService,\
        LogService,\
        ResponseService

    service = TaleService()
    service = PathService(paths = {'session': service})
    service = AdhocKitService(service)
    #service = LogService(service)
    service = ResponseService(service)
    serve(service, port = 2380, debug = True)

