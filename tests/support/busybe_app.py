import os
import subprocess
import time
from os import path


class FrontApi:

    def __init__(self):
        self._app_p = None

    def start(self):
        self._start_app()

    def _start_app(self):
        app_env = os.environ.copy()
        app_file = os.getcwd().split('tests')[0] + 'service/api.py'
        if not path.exists(app_file):
            app_file = 'service/api.py'

        self._app_p = subprocess.Popen(
            ['python', app_file], env=app_env)

        # need to wait for the service to start
        time.sleep(2)

    def stop(self):
        print('Terminating app')
        self._app_p.terminate()  # Use terminate instead of kill
        self._app_p.wait()  # Wait for the process to terminate completely
        print('App terminated')
