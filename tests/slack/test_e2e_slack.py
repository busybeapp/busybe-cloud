import pytest
from busypie import wait
from hamcrest import assert_that, equal_to, has_item, has_property
from random_word import RandomWords


@pytest.mark.asyncio
async def test_create_new_entry_via_slack(app, slack):
    title = RandomWords().get_random_word()
    app.send_slack_shortcut_message(build_request(title))
    entries = app.get_entries()
    assert_that(entries, has_item(has_property("title", equal_to(title))))


def build_request(title):
    return {
        "user": {"name": "busybe_tester"},
        "message": {"text": title},
        "response_url": "http://localhost:9090/webhook"
    }


@pytest.mark.asyncio
async def test_callback_msg_to_slack(app, slack):
    title = RandomWords().get_random_word()
    app.send_slack_shortcut_message(build_request(title))
    msg = wait().until(lambda: slack.get_callback_msg())
    assert_that(msg, equal_to(f"{title} was added to your busybe inbox"))
