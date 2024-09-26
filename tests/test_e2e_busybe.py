import pytest
from hamcrest import assert_that, equal_to, is_not, has_items

from tests.support.app import App


@pytest.fixture(scope='session')
def app():
    app = App()
    app.start()
    yield app
    app.stop()


def test_is_healthy(app):
    assert app.is_healthy()


def test_create_new_entry(app):
    title = 'task 1'
    entry = app.create_entry(title)
    assert_that(entry.id, is_not(None))
    assert_that(entry.title, equal_to(title))


def test_raise_bad_request_while_creating_entry_without_title(app):
    with pytest.raises(AssertionError, match="status code: 400"):
        app.create_entry('')


def test_all_entries_received(app):
    entry_one = app.create_entry('task 1')
    entry_two = app.create_entry('task 2')
    entries = app.get_entries()
    assert_that(entries, has_items(equal_to(entry_one), equal_to(entry_two)))


# def test_create_new_entry_via_slack(app):
#     title = 'Slack task 1'
#     response, response_json = app_driver.create_task_via_slack(title)
#
#     assert_that(response.status_code, equal_to(200))
#     assert_that(response_json['text'], equal_to(f"Task created: {title}"))
#
#
# def test_list_tasks_via_slack(app):
#     app_driver.create_task_via_slack('Slack task 1')
#     app_driver.create_task_via_slack('Slack task 2')
#
#     response, response_json = app_driver.list_tasks_via_slack()
#     task_list = response_json['text']
#
#     assert_that(response.status_code, equal_to(200))
#     assert_that(task_list, is_('Here are your tasks:\nSlack task 1\nSlack task 2'))
#
#
# def test_invalid_slack_token(app):
#     title = 'Invalid token task'
#     response, response_json = app_driver.send_invalid_token("/busybe", title)
#
#     assert_that(response.status_code, equal_to(401))
#     assert_that(response_json['detail'], equal_to("Invalid token"))