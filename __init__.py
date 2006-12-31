
from cixar.ish.lazy import ShellService, ShellClientService, CommonCommands
from cixar.ish.command import CommandMode, command, alias

class Mode(CommandMode):

    class Commands(CommonCommands):

        @command()
        def hi(self):
            tags = self.kit.tags
            self.message(tags.b('Hi'))

        exit = None

class ClientService(ShellClientService):
    pass

class TaleService(ShellService):
    Mode = Mode
    ClientService = ClientService

