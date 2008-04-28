
from planes.lazy import PathService, FileTreeService, FileService, Response, SessionService, JsonService, JsonReaderService, JsonWriterService, FunctionService

import tale
import planes.chiron
from planes.python.module_path import module_path
from xml.sax.saxutils import escape

def TaleService():

    messages = []

    def Session():

        base_n = len(messages)

        def respond(kit, n):
            if kit.session_lost:
                pass
            n = int(n)
            return {
                'messages': [
                    {
                        'n': n,
                        'html': escape(messages[n - base_n]),
                    }
                    for n in range(base_n, len(messages) - base_n)
                ],
            }

        def command(command):
            if command == '/night':
                pass
            else:
                messages.append(command)

        @JsonService
        def command_service(kit, object):
            command(object['command'])
            return respond(kit, object['n'])

        @JsonService
        def messages_service(kit, n):
            return respond(kit, n)

        return PathService(
            paths = {
                'command': command_service,
            },
            next_service = messages_service,
        )

    session_service = SessionService(Session)
    return session_service

