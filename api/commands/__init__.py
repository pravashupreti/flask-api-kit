from flask import Flask

from api.commands.auth import auth_cli

_COMMANDS = [
    auth_cli
]


def register_commands(app: Flask):    
    for command in _COMMANDS:
        app.cli.add_command(command)
