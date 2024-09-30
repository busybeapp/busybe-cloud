import pytest
from hamcrest import assert_that, is_

from service.entries.model.entry import Entry


def test_convert_valid_json_to_entry():
    title = 'kuku'
    entry = Entry.from_json({'title': title})
    assert isinstance(entry, Entry)
    assert_that(entry.title, is_(title))
    assert_that(entry.id, is_(None))


def test_raise_value_error_given_invalid_json():
    with pytest.raises(ValueError):
        Entry.from_json({'id': '1234'})


def test_convert_entry_to_json():
    entry_json = Entry(id='12345', title='kuku_task').to_json()
    assert_that(entry_json, is_({'id': '12345', 'title': 'kuku_task'}))