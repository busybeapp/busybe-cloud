import pytest
from hamcrest import assert_that, equal_to, is_

from tests.support.busybe_app import App
from tests.support.driver import Driver


app_driver = Driver()


@pytest.fixture(scope='function')
def app():
    app = App()
    app.start()
    yield app
    app.stop()


def test_is_healthy(app):
    assert app_driver.is_healthy()


def test_create_new_entry(app):
    title = 'task 1'
    response = app_driver.create_entry(title)
    assert_that(response.title, equal_to(title))


def test_raise_bad_request_while_creating_entry_without_title(app):
    app_driver.create_entry('', expected_bad_request=True)


def test_all_entries_received(app):
    entry_one = app_driver.create_entry('task 1')
    entry_two = app_driver.create_entry('task 2')
    entries = app_driver.get_entries()

    found_first = False
    found_second = False

    for entry in entries:
        if entry.id == entry_one.id and entry.title == 'task 1':
            found_first = True
        if entry.id == entry_two.id and entry.title == 'task 2':
            found_second = True

    assert_that(found_first, is_(True))
    assert_that(found_second, is_(True))

