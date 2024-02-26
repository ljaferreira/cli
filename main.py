import platform

import click
import re

from linux import Linux
from windows import Windows


@click.group()
def cli():
    pass


@cli.group()
def workspace():
    pass


@workspace.command()
@click.option('--username', prompt='Username ')
def start(username):
    global os
    if not re.match(r"\w\d{6}", username):
        click.echo(
            click.style(
                f"😞 Username invalid!",
                fg="red",
            )
        )
        return
    os = Windows()

    if platform.system() == 'Linux':
        os = Linux()

    os.start(username)


@workspace.command()
@click.option('--username', prompt='Username ')
def stop(username):
    global os
    if not re.match(r"\w\d{6}", username):
        click.echo(
            click.style(
                f"😞 Username invalid!",
                fg="red",
            )
        )
        return
    os = Windows()

    if platform.system() == 'Linux':
        os = Linux()

    os.stop(username)


if __name__ == "__main__":
    cli()
