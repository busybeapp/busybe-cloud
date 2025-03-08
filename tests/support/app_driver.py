import os
import subprocess
from busypie import wait as busy_wait
from tests.support.client import Client


class AppDriver:

    def __init__(self):
        self._app_p = None
        self.app_client = None

    def start(self):
        self.app_client = Client()
        self._start_app()

    def _start_app(self):
        app_file = os.getcwd().split('tests')[0] + 'service/app.py'
        if not os.path.exists(app_file):
            app_file = 'service/app.py'

        self._app_p = subprocess.Popen(
            ['python', app_file], env=(os.environ.copy())
        )

        busy_wait().ignore_exceptions().until(self.is_healthy)

    def stop(self):
        self._app_p.terminate()
        self._app_p.wait()

    def is_healthy(self, headers=None):
        return self.app_client.is_healthy(headers)

    def create_entry(self, title):
        return self.app_client.create_entry(title)

    def get_entries(self):
        return self.app_client.get_entries()

    def send_slack_shortcut_message(self, data):
        return self.app_client.send_slack_message_shortcut(data)

    def valid_user_login(self):
        return self.app_client.login("Creeper")

    def unauthorized_user_login(self):
        return self.app_client.login("BadLord")
