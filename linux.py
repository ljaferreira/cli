import click


class Linux:
    def __init__(self):
        pass

    def login(self):
        import subprocess

        print("check if gcloud is logged in")
        if subprocess.run(["gcloud", "config", "get-value", "account"], stdout=subprocess.PIPE).stdout:
            click.echo(
                click.style(
                    "you are logged in",
                    fg="green",
                )
            )
        else:
            subprocess.run(["gcloud", "auth", "login"])
            click.echo(
                click.style(
                    "login successfully",
                    fg="green",
                )
            )

    def start(self, username):
        import os
        import subprocess
        import time
        from utils import kill_older_process

        click.echo("check trust host is configured")
        if os.path.exists("~/.ssh/config"):
            if not any("Host *" in line for line in open(os.path.expanduser("~/.ssh/config"))):
                with open(os.path.expanduser("~/.ssh/config"), "w") as config_file:
                    config_file.write("Host *\n")
                    config_file.write("    StrictHostKeyChecking no\n")

        click.echo('killing older processes')
        kill_older_process(4022)

        self.login()

        try:
            result = subprocess.run(
                ["gcloud", "workstations", "start", f"ws-{username}", "--project=sas-eng-suptengb-sbx",
                 "--region=us-central1",
                 "--cluster=poc", "--config=ws-config-poc"], stderr=subprocess.DEVNULL).returncode
            if result > 0:
                raise Exception('unable to start workstation')

            click.echo(
                click.style(
                    "workstation started",
                    fg="green",
                )
            )

            result = subprocess.run(
                ["gcloud", "workstations", "start-tcp-tunnel", "--quiet", "--project=sas-eng-suptengb-sbx",
                 "--region=us-central1", "--cluster=poc", "--config=ws-config-poc",
                 "--local-host-port=:4022",
                 f"ws-{username}", "22"]).returncode
            if result > 0:
                raise Exception('unable to connect workstation')

            command = (f'gcloud workstations start-tcp-tunnel --quiet --project=sas-eng-suptengb-sbx '
                       f'--region=us-central1 --cluster=poc --config=ws-config-poc --local-host-port=:4022 '
                       f'ws-{username} 22 &')

            os.system(command)

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
            while not subprocess.run(["lsof", "-Pi", ":4022", "-sTCP:LISTEN"], stdout=subprocess.PIPE).stdout:
                time.sleep(5)
                print("waiting for ssh tunnel to start")

                subprocess.run(["code", "--remote=ssh-remote+localhost:4022", "/home/user"])

    def stop(self, username):
        import subprocess
        from utils import kill_older_process

        click.echo('killing older processes')
        kill_older_process(4022)
        try:
            result = subprocess.run(
                ["gcloud", "workstations", "stop", f"ws-{username}", "--project=sas-eng-suptengb-sbx",
                 "--region=us-central1",
                 "--cluster=poc", "--config=ws-config-poc"], stderr=subprocess.DEVNULL).returncode
            if result > 0:
                raise Exception('unable to start workstation')

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