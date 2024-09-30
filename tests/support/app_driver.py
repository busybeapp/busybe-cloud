import os
import subprocess

from busypie import wait as busy_wait, SECOND

from tests.support.driver import Driver


class AppDriver:

    def __init__(self):
        self._app_p = None
        self.driver = None

    def start(self):
        self.driver = Driver()
        self._start_app()

    def _start_app(self):
        self._app_p = subprocess.Popen(
            ['python', 'service/app.py'], env=(os.environ.copy())
        )

        (busy_wait().
         ignore_exceptions().
         at_most(30 * SECOND).
         poll_interval(2 * SECOND).
         until(lambda: self.is_healthy()))

    def stop(self):
        print('Terminating app')
        self._app_p.terminate()
        self._app_p.wait()
        print('App terminated')

    def is_healthy(self):
        return self.driver.is_healthy()

    def create_entry(self, title):
        return self.driver.create_entry(title)

    def get_entries(self):
        return self.driver.get_entries()

    def create_task_via_slack(self, title):
        return self.driver.create_task_via_slack(title)

    def list_tasks_via_slack(self):
        return self.driver.list_tasks_via_slack()

    def send_invalid_token(self, command, text):
        return self.driver.send_invalid_token(command, text)

