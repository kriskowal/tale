
from tale.world import Event, Say, Move, Direction

def do(self, command):
    if command.startswith('"'):
        command = command[1:]
        return chat(self, command)
    else:
        if ' ' in command:
            command, argument = command.split(' ', 1)
        else:
            argument = None
        if command == 'help':
            self.session.send({'html': "Meh, you'll figure it out."})
        elif command in Direction.directions:
            self.player.request(Move(self.player, Direction.directions[command]))
        elif command == 'i':
            command = argument
            do_(self, Event.events_by_nominative, command)
        elif command == 'me':
            command = argument
            do_(self, Event.events_by_present, command)
        elif command in Event.events_by_nominative:
            Command = Event.events_by_nominative[command]
            argument = Command.lookup(self.player.narrative, argument)
            if argument is None:
                self.player.request(Command(self.player))
            else:
                self.player.request(Command(self.player, argument))
        else:
            self.session.send({'html': escape("You can't do that.")})

def do_(self, commands, command):
        if ' ' in command:
            command, argument = command.split(' ', 1)
        else:
            argument = None
        if command in commands:
            Command = commands[command]
            argument = Command.lookup(self.player.narrative, argument)
            if argument is None:
                self.player.request(Command(self.player))
            else:
                self.player.request(Command(self.player, argument))
        else:
            self.session.send({'html': escape("You can't do that.")})

def chat(self, command):
    if command.startswith('/'):
        command = command[1:]
        return do(self, command)
    else:
        self.player.request(Say(self.player, command))

