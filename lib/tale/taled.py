
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

class TaleSession(PathService):

    def __init__(self):

        self.messages = []
        self.requests = []

        def command(request, command):
            self.output(command)

        def command_service(request, object):
            command(request, object['command'])
            poll_service(request, object)

        def poll_service(request, object):
            self.requests.insert(0, request)
            return self.respond()

        def push_service(request):
            if request.session_lost:
                return 'new session'
            else:
                self.requests.append(request)

        super(TaleSession, self).__init__(
            paths = {
                'command': JsonRequestService(command_service),
                'poll': JsonRequestService(poll_service),
                'push': push_service,
            },
            service = poll_service,
        )

    def get_messages(self):
        response = {
            'messages': [
                {
                    'html': escape(self.messages[n]),
                }
                for n in range(0, len(self.messages))
            ],
        }
        self.messages[:] = []
        return response

    def respond(self):
        if self.requests:
            request = self.requests.pop(0)
            response = self.get_messages()
            request.output.write(simplejson.dumps(response))
            request.finish()

    def output(self, message):
        self.messages.append(message)

def TaleService():
    session_service = SessionService(TaleSession)
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


