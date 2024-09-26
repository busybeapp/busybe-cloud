import threading
import uuid

from service.entries.model.entry import Entry


class EntriesStore:

    def __init__(self):
        self.entries = {}
        self.mu = threading.Lock()

    def add_entry(self, entry):
        entry = Entry.from_json(entry)

        entry.id = self.create_id()

        with self.mu:
            self.entries[entry.id] = entry
        return entry

    def get_entries(self):
        with self.mu:
            return [entry.to_json() for entry in self.entries.values()]

    @staticmethod
    def create_id():
        return str(uuid.uuid4())
