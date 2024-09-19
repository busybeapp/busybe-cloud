from http.client import ACCEPTED, CREATED, BAD_REQUEST

import requests

from service.entries.model.entry import Entry


class Driver:

    @staticmethod
    def is_healthy():
        response = requests.get("http://localhost:8080/api/health", verify=False)
        return response.status_code == ACCEPTED.value

    @staticmethod
    def post_entry(param):
        response = requests.post("http://localhost:8080/api/entries", json={'title': param})
        assert response.status_code == CREATED.value
        return Entry.from_json(response.json())

    @staticmethod
    def post_entry_expecting_bad_request(param):
        response = requests.post("http://localhost:8080/api/entries", json={'title': param})
        return response.status_code == BAD_REQUEST.value

    @staticmethod
    def get_entries():
        response = requests.get("http://localhost:8080/api/entries")
        assert response.status_code == ACCEPTED.value
        return [Entry.from_json(entry) for entry in response.json()]


