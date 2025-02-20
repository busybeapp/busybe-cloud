import re

import pytest
from hamcrest import assert_that, is_, is_not

from service.entries.persistence.entries_store import EntriesStore


@pytest.fixture(scope="function")
def entries_store():
    store = EntriesStore()
    store.clear()
    return store


def test_entry_id_is_uuid(entries_store):
    entry = entries_store.add_entry({"title": "Entry one"})
    _assert_is_uuid(entry.id)


def _assert_is_uuid(_id):
    pattern = (r'^[{]?([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]'
               r'{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})[}]?$')
    assert_that(bool(re.match(pattern, _id)), is_(True))


def test_entry_ids_are_different(entries_store):
    entry_one = entries_store.add_entry({"title": "Entry one"})
    entry_two = entries_store.add_entry({"title": "Entry two"})
    assert_that(entry_one.id, is_not(entry_two.id))


def test_get_entries(entries_store):
    entries_store.add_entry({"title": "Entry one"})
    entries_store.add_entry({"title": "Entry two"})
    assert_that(len(entries_store.get_entries()), is_(2))
