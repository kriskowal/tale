
from planes.lazy import\
    PathService,\
    FileTreeService,\
    FileService,\
    Response,\
    SessionService,\
    JsonService,\
    JsonReaderService,\
    JsonWriterService,\
    FunctionService

import tale
import planes.chiron
from planes.python.module_path import module_path
from xml.sax.saxutils import escape

class TaleSession(PathService):

    def __init__(self):

        self.messages = []

        def respond(kit, n):
            if kit.session_lost:
                pass
            n = int(n)
            return {
                'messages': [
                    {
                        'n': n,
                        'html': escape(self.messages[n]),
                    }
                    for n in range(0, len(self.messages))
                ],
            }

        def command(kit, command):
            if command == '/night':
                pass
            else:
                self.broadcast(kit, command)

        @JsonService
        def command_service(kit, object):
            command(kit, object['command'])
            return respond(kit, object['n'])

        @JsonService
        def messages_service(kit, n):
            return respond(kit, n)

        super(TaleSession, self).__init__(
            paths = {'command': command_service,},
            service = messages_service,
            next_service = messages_service,
        )

    def output(self, kit, message):
        self.messages.append(message)

    def broadcast(self, kit, message):
        for session_id, session in self.session_service.sessions.items():
            if session_id == kit.session_id:
                session.service.output(kit, "you: %s" % message)
            else:
                session.service.output(kit, "%s: %s" % (kit.session_id[:4], message))

def TaleService():
    session_service = SessionService(TaleSession)
    return session_service

