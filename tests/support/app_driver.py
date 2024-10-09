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

    def is_healthy(self):
        return self.app_client.is_healthy()

    def create_entry(self, title):
        return self.app_client.create_entry(title)

    def get_entries(self):
        return self.app_client.get_entries()

    def create_task_via_slack(self, title):
        return self.app_client.create_task_via_slack(title)

    def send_invalid_token(self):
        return self.app_client.send_invalid_token()

    def send_unrecognized_command(self):
        return self.app_client.send_unrecognized_command()