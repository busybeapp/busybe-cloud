import threading
import uuid

from service.entries.model.entry import Entry


class EntriesStore:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(EntriesStore, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.entries = {}
            self.mu = threading.Lock()
            self.initialized = True

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
