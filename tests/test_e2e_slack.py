import pytest
from hamcrest import assert_that, equal_to, is_not

from service.slack.slack_content_messages import (SLACK_TEXT_INVALID_TOKEN,
                                                  SLACK_TEXT_COMMAND_NOT_RECOGNIZED,
                                                  SLACK_TEXT_PROVIDE_TASK_TITLE)
from tests.support.app_driver import AppDriver


@pytest.fixture(scope='session')
def app():
    app = AppDriver()
    try:
        app.start()
        yield app
    finally:
        app.stop()


def test_create_new_entry_via_slack(app):
    entry = app.create_task_via_slack('New task')
    assert_that(entry['text'], equal_to('Task created: New task'))
    assert_that(entry['id'], is_not(None))


def test_fail_create_entry_with_no_title(app):
    entry = app.create_task_via_slack('')
    assert_that(entry['text'], equal_to(SLACK_TEXT_PROVIDE_TASK_TITLE))


def test_fail_invalid_slack_token(app):
    entry = app.send_invalid_token()
    assert_that(entry['detail'], equal_to(SLACK_TEXT_INVALID_TOKEN))


def test_unrecognized_command(app):
    entry = app.send_unrecognized_command()
    assert_that(entry['text'], equal_to(SLACK_TEXT_COMMAND_NOT_RECOGNIZED))
