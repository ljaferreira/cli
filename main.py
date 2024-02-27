import click

from utils import validate_username,verify_platform


@click.group()
def cli():
    pass


@cli.command()
def login():
    os = verify_platform()
    os.login()


@cli.group()
def workspace():
    pass

@workspace.command()
@click.option('--username', prompt='Username ')
def start(username):
    validate_username(username)
    os = verify_platform()
    os.start(username)


@workspace.command()
@click.option('--username', prompt='Username ')
def stop(username):
    validate_username(username)
    os = verify_platform()
    os.stop(username)


if __name__ == "__main__":
    cli()
