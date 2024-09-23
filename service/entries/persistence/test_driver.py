from unittest.mock import patch

import pytest
from hamcrest import assert_that, is_

from service.entries.persistence.entries_driver import EntriesDriver


@pytest.fixture
def entries_driver():
    return EntriesDriver()


@patch('service.entries.persistence.id_manager.IdManager.assign')
def test_add_entry(id_assign, entries_driver):
    entry = {
        "title": "kuku popo"
    }
    expected_id = id_assign.return_value = '123'
    saved_entry = entries_driver.add_entry(entry)
    assert_that(saved_entry.id, is_('123'))
    assert_that(saved_entry.title, is_(entry["title"]))
    assert_that(entries_driver.entries.get(expected_id).title, is_('kuku popo'))


def test_get_entries(entries_driver):
    entries_driver.add_entry({"title": "Entry one"})
    entries_driver.add_entry({"title": "Entry two"})
    assert_that(len(entries_driver.get_entries()), is_(2))
