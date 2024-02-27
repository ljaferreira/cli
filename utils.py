import psutil
import re
import click
from linux import Linux
from windows import Windows
import platform


def get_pid(port):
    connections = psutil.net_connections()
    for con in connections:
        if con.raddr != tuple():
            if con.raddr.port == port:
                return con.pid, con.status
        if con.laddr != tuple():
            if con.laddr.port == port:
                return con.pid, con.status
    return 0, None


def kill_older_process(port: int):
    pid, _ = get_pid(port)
    if pid is None or pid > 0:
        p = psutil.Process(pid)
        p.terminate()


def validate_username(username):
    if not re.match(r"\w\d{6}", username):
        click.echo(
            click.style(
                f"😞 Username invalid!",
                fg="red",
            )
        )
        return False
    return True


def verify_platform():
    os = Windows()

    if platform.system() == 'Linux':
        os = Linux()
    return os
