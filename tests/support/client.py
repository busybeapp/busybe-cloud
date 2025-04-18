import json
import os

import requests
from hamcrest import assert_that, is_

from service.entries.model.entry import Entry

AUTH_ERROR = "Login failed"


class LoginException(Exception):
    def __init__(self, status_code, message=AUTH_ERROR):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)


class Client:

    def __init__(self, token=None):
        self.port = os.getenv("PORT", 8080)
        self.endpoint = os.getenv("ENDPOINT", 'localhost')
        self.root = f'http://{self.endpoint}:{self.port}'
        self.slack_token = os.getenv("SLACK_VERIFICATION_TOKEN")

    def is_healthy(self, headers=None):
        response = requests.get(f"{self.root}/health",
                                verify=False,
                                headers=headers)
        if response.status_code == 403:
            assert_that(response.status_code, is_(403),
                        "CORS policy does not allow this origin")
        else:
            assert_that(response.status_code, is_(200))
        return response

    def create_entry(self, entry_title, token=None):
        response = requests.post(f"{self.root}/api/entries",
                                 json={'title': entry_title},
                                 headers=(self._append_token(token)))
        assert response.status_code == 201, response.status_code
        return Entry.from_json(response.json())

    def get_entries(self, token=None):
        response = requests.get(f"{self.root}/api/entries",
                                headers=(self._append_token(token)))
        assert response.status_code == 200
        return [Entry.from_json(entry) for entry in response.json()]

    @staticmethod
    def _append_token(token):
        headers = {
            'Authorization': f'Bearer {token}'
        }
        return headers

    def send_slack_message_shortcut(self, data, invalid_token=False):
        data['token'] = invalid_token if invalid_token else self.slack_token

        payload = {
            "payload": json.dumps(data)
        }

        response = requests.post(
            f"{self.root}/api/slack/message-shortcut",
            data=payload)

        assert response.status_code == (401 if invalid_token else 200)

        return response.json()

    def login(self, secret):
        response = requests.post(f"{self.root}/api/login",
                                 json={"secret": secret})
        if response.status_code != 200:
            raise LoginException(response.status_code)

        return response.json()
