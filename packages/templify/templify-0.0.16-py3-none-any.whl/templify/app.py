import sys

from templify.services import from_django


def main():
    commands = sys.argv[1:]
    commands_count = len(commands)
    if not commands_count:
        return "Hello from Templify"
    if commands_count == 1 and commands[0] == 'from_django':
        return from_django()
    if commands_count == 1 and commands[0] == 'start':
        return from_django()
    else:
        return 'Command not found'


if __name__ == "__main__":
    main()
