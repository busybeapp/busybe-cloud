import os
from http.client import ACCEPTED, CREATED, BAD_REQUEST

import requests
from dotenv import load_dotenv

from service.entries.model.entry import Entry

load_dotenv()


class Driver:

    def __init__(self):
        self.port = os.getenv("PORT", 8080)
        self.endpoint = os.getenv("ENDPOINT", 'localhost')
        self.root = f'http://{self.endpoint}:{self.port}/api'

    def is_healthy(self):
        response = requests.get(f"{self.root}/health", verify=False)
        return response.status_code == ACCEPTED

    def create_entry(self, entry_title, expected_bad_request=False):
        response = requests.post(f"{self.root}/entries", json={'title': entry_title})

        if expected_bad_request:
            assert response.status_code == BAD_REQUEST
        else:
            assert response.status_code == CREATED
            return Entry.from_json(response.json())

    def get_entries(self):
        response = requests.get(f"{self.root}/entries")
        assert response.status_code == ACCEPTED
        return [Entry.from_json(entry) for entry in response.json()]


