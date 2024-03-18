import os
import sys
import click
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from thunder.get_latest import get_latest

# URLs for cloud functions
CREATE_SESSION_USER_URL = "https://create-session-user-mumhtj6swa-uc.a.run.app"
DELETE_SESSION_USER_URL = "https://delete-session-user-mumhtj6swa-uc.a.run.app"


# Helper to call cloud functions
def call_firebase_function(url, id_token, payload=None):
    headers = {
        "Authorization": "Bearer " + id_token,
        "Content-Type": "application/json",
    }

    response = requests.post(url, headers=headers, json=payload, timeout=5)
    return response


class Task:
    def __init__(self, ngpus: int, args: tuple, uid: str):
        self.ngpus = ngpus
        self.args = args[0].split(" ")
        self.username = uid
        self.password = None
        self.topic = None

    # set environment variable for
    # use firebase credentials to retrieve session password
    def get_password(self, id_token: str) -> bool:
        payload = {}
        response = call_firebase_function(CREATE_SESSION_USER_URL, id_token, payload)
        if response.status_code != 200:
            click.echo("Failed to create user.")
            return False
        response = response.json()
        if not isinstance(response, dict):
            click.echo("Failed to create user.")
            return False

        password = response.get("password")

        if not password:
            click.echo("Invalid response: Password missing.")
            return False

        self.password = password
        return True

    def execute_task(self, id_token: str) -> bool:
        # to implement, communicate to manager that a task is beginning, triggering start_user
        # look up python os.fork process set environment variables
        click.echo("executing task")

        # We need to find the shared object
        # binary = "/thunder/client_linux_x86_64"
        # if not os.path.exists("/thunder/client_linux_x86_64"):
        #     click.echo("thunder.so file not found")
        #     return False

        # Get from https://storage.googleapis.com/thunder_binary/client
        binary = get_latest("client", "/root/thunder.so")
        if binary == None:
            print("Failed to download binary")
            return False

        os.environ["SESSION_USERNAME"] = self.username
        os.environ["SESSION_PASSWORD"] = self.password
        os.environ["TOKEN"] = id_token
        os.environ["LD_PRELOAD"] = binary

        # This should never return
        os.execvp(self.args[0], self.args)
        return False

    def close_session(self, id_token: str) -> bool:
        # to implement, communicate to manager computation is done, triggering exit_user
        click.echo("finishing task")
        return True
