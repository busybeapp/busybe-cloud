import threading

from service.entries.model.entry import Entry
from service.entries.persistence.id_manager import IdManager


class EntriesDriver:

    def __init__(self):
        self.entries = {}
        self.mu = threading.Lock()

    def add_entry(self, entry):
        entry = Entry.from_json(entry)

        entry.id = IdManager.assign()

        with self.mu:
            self.entries[entry.id] = entry
        return entry

    def get_entries(self):
        with self.mu:
            return [entry.to_json() for entry in self.entries.values()]
