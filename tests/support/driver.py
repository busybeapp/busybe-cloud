import os

import requests

from service.entries.model.entry import Entry


class Driver:

    def __init__(self):
        self.port = os.getenv("PORT", 8080)
        self.endpoint = os.getenv("ENDPOINT", 'localhost')
        self.root = f'http://{self.endpoint}:{self.port}'
        self.slack_token = os.getenv("SLACK_VERIFICATION_TOKEN", "your-slack-verification-token")

    def is_healthy(self):
        response = requests.get(f"{self.root}/health", verify=False)
        return response.status_code == 200

    def create_entry(self, entry_title):
        response = requests.post(f"{self.root}/api/entries", json={'title': entry_title})
        assert response.status_code == 201, response.status_code
        return Entry.from_json(response.json())

    def get_entries(self):
        response = requests.get(f"{self.root}/api/entries")
        assert response.status_code == 200
        return [Entry.from_json(entry) for entry in response.json()]

    def create_task_via_slack(self, title):
        return self._send_slack_command("/busybe", title)

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
        return self._send_slack_command("/listentries", "")

    def send_invalid_token(self, command, text):
        return self._send_slack_command(command, text, token="invalid_token")