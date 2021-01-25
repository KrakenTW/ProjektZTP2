import time
from abc import ABCMeta, abstractstaticmethod


class ICommand(metaclass=ABCMeta):
    """The command interface, which all commands will implement"""

    @abstractstaticmethod
    def execute():
        """The required execute method which all command obejcts will use"""


class Invoker:
    """The Invoker Class"""

    def __init__(self):
        self._commands = {}

    def register(self, command_name, command):
        self._commands[command_name] = command

    def execute(self, command_name):
        if command_name in self._commands.keys():
            self._commands[command_name].execute()
        else:
            print(f"Command [{command_name}] not recognised")


class InvokerMoveLeft(ICommand):
    """A Command object, which implemets the ICommand interface"""

    def __init__(self, statekGracza):
        self._statekGracza = statekGracza

    def execute(self):
        self._statekGracza.move_left()


class InvokerMoveRight(ICommand):
    """A Command object, which implemets the ICommand interface"""

    def __init__(self, statekGracza):
        self._statekGracza = statekGracza

    def execute(self):
        self._statekGracza.move_right()


if __name__ == "__main__":
    # The Client is the main python app

    # The Light is the Reciever
    LIGHT = Light()

    # Create Commands
    Invoker_move_left = InvokerMoveLeft(StatekGracza)
    Invoker_move_right = InvokerMoveRight(StatekGracza)

    # Register the commands with the invoker (Invoker)
    Invoker = Invoker()
    Invoker.register(pygame.K_LEFT, Invoker_move_left)
    Invoker.register(pygame.K_RIGHT, Invoker_move_right)

    # Execute the commands that are registered on the Invoker
    Invoker.execute("ON")
    Invoker.execute("OFF")
    Invoker.execute("ON")
    Invoker.execute("OFF")
