import pytest
from hamcrest import assert_that, equal_to, is_not, has_items
from starlette import status

from tests.support.app_driver import AppDriver


@pytest.fixture(scope='session')
def app():
    app = AppDriver()
    try:
        app.start()
        yield app
    finally:
        app.stop()


def test_is_healthy(app):
    assert app.is_healthy()


def test_create_new_entry(app):
    title = 'task 1'
    entry = app.create_entry(title)
    assert_that(entry.id, is_not(None))
    assert_that(entry.title, equal_to(title))


def test_raise_bad_request_while_creating_entry_without_title(app):
    with pytest.raises(AssertionError, match=str(status.HTTP_400_BAD_REQUEST)):
        app.create_entry('')


def test_all_entries_received(app):
    entry_one = app.create_entry('task 1')
    entry_two = app.create_entry('task 2')
    entries = app.get_entries()
    assert_that(entries, has_items(equal_to(entry_one), equal_to(entry_two)))
