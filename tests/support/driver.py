import os
from http.client import ACCEPTED, CREATED, BAD_REQUEST, OK

import requests
from dotenv import load_dotenv

from service.entries.model.entry import Entry

load_dotenv()


class Driver:

    def __init__(self):
        self.port = os.getenv("PORT", 8080)
        self.endpoint = os.getenv("ENDPOINT", 'localhost')
        self.root = f'http://{self.endpoint}:{self.port}/api'
        self.slack_token = "your-slack-verification-token"

    def is_healthy(self):
        response = requests.get(f"{self.root}/health", verify=False)
        return response.status_code == OK

    def create_entry(self, entry_title, expected_bad_request=False):
        response = requests.post(f"{self.root}/entries", json={'title': entry_title})

        if expected_bad_request:
            assert response.status_code == BAD_REQUEST
        else:
            assert response.status_code == CREATED
            return Entry.from_json(response.json())

    def get_entries(self):
        response = requests.get(f"{self.root}/entries")
        assert response.status_code == OK
        return [Entry.from_json(entry) for entry in response.json()]

    def create_task_via_slack(self, title):
        return self._send_slack_command("/busybe", title, token=os.getenv('SLACK_VERIFICATION_TOKEN'))

    def _send_slack_command(self, command, text, token=None):
        if token is None:
            token = self.slack_token

        response = requests.post(f"{self.root}/slack/events", data={
            "command": command,
            "text": text,
            "token": token
        })

        response_json = response.json()
        return response, response_json

    def list_tasks_via_slack(self):
        return self._send_slack_command("/listentries", "", token=os.getenv('SLACK_VERIFICATION_TOKEN'))

    def send_invalid_token(self, command, text):
        return self._send_slack_command(command, text, token="invalid_token")