import pytest
from hamcrest import assert_that, equal_to, is_

from tests.support.busybe_app import FrontApi
from tests.support.driver import Driver


@pytest.fixture(scope='function')
def busybe_app():
    app = FrontApi()
    app.start()
    yield app
    app.stop()


def test_is_healthy(busybe_app):
    assert Driver.is_healthy()


def test_create_new_entry(busybe_app):
    title = 'task 1'
    response = Driver.create_entry(title)
    assert_that(response.title, equal_to(title))


def test_raise_bad_request_while_creating_entry_without_title(busybe_app):
    assert Driver.post_entry_expecting_bad_request('')


def test_all_entries_received(busybe_app):
    entry_one = Driver.create_entry('task 1')
    entry_two = Driver.create_entry('task 2')
    entries = Driver.get_entries()

    found_first = False
    found_second = False

    for entry in entries:
        if entry.id == entry_one.id and entry.title == 'task 1':
            found_first = True
        if entry.id == entry_two.id and entry.title == 'task 2':
            found_second = True

    assert_that(found_first, is_(True))
    assert_that(found_second, is_(True))

