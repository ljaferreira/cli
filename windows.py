import click


class Windows:
    def __init__(self):
        pass

    def login(self):
        import os
        from subprocess import Popen
        from subprocess import PIPE


        click.echo("check if gcloud is logged in")
        command = 'gcloud config get-value account'
        pipe = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)

        line = pipe.stdout.readline()

        if line:
            click.echo(
                click.style(
                    "you are logged in",
                    fg="green",
                )
            )
        else:
            command = 'gcloud auth login'
            os.system(command)
            click.echo(
                click.style(
                    "login successfully",
                    fg="green",
                )
            )

    def start(self, username):
        import os
        import time
        from utils import kill_older_process
        from subprocess import Popen
        import socket as sock

        click.echo("check trust host is configured")
        click.echo(f'{os.environ.get("HOMEPATH")}\.ssh\config')
        if os.path.exists(f'{os.environ.get("HOMEPATH")}\.ssh\config'):
            if not any("Host *" in line for line in open(os.path.expanduser(f'{os.environ.get("HOMEPATH")}\.ssh\config'))):
                with open(os.path.expanduser(f'{os.environ.get("HOMEPATH")}/.ssh/config'), "w") as config_file:
                    config_file.write("Host *\n")
                    config_file.write("    StrictHostKeyChecking no\n")

        click.echo('killing older processes')
        kill_older_process(4022)

        self.login()

        try:
            click.echo(
                click.style(
                    "starting workstation",
                    fg="green",
                )
            )
            command = (f"gcloud workstations start ws-{username} --project=sas-eng-suptengb-sbx --region=us-central1 "
                       f"--cluster=poc --config=ws-config-poc")
            os.system(command)

            click.echo(
                click.style(
                    "workstation started",
                    fg="green",
                )
            )

            click.echo(
                click.style(
                    "creating tunnel",
                    fg="green",
                )
            )

            command = (f'gcloud workstations start-tcp-tunnel --quiet --project=sas-eng-suptengb-sbx '
                       f'--region=us-central1 --cluster=poc --config=ws-config-poc --local-host-port=:4022 '
                       f'ws-{username} 22 &')

            Popen(command, shell=True)

            click.echo(
                click.style(
                    "tunnel created",
                    fg="green",
                )
            )

        except Exception as e:
            click.echo(
                click.style(
                    f"😞 {e}!",
                    fg="red",
                )
            )

        else:
            print("waiting for ssh tunnel to start")
            create_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
            destination = ("127.0.0.1", 4022)
            while create_socket.connect_ex(destination) == 0:
                time.sleep(5)
                print("waiting for ssh tunnel to start")

            os.system("code --remote=ssh-remote+localhost:4022 /home/user")

    def stop(self, username):
        from utils import kill_older_process
        from subprocess import Popen
        from subprocess import PIPE

        click.echo('killing older processes')
        kill_older_process(4022)

        try:
            command = (f"gcloud workstations stop ws-{username} --project=sas-eng-suptengb-sbx --region=us-central1 "
                       f"--cluster=poc --config=ws-config-poc")

            Popen(command, shell=True, stdout=PIPE, stderr=PIPE)

            click.echo(
                click.style(
                    "workstation stopped",
                    fg="green",
                )
            )

        except Exception as e:
            click.echo(
                click.style(
                    f"😞 {e}!",
                    fg="red",
                )
            )
