import pytest
from dotenv import load_dotenv

from tests.support.app_driver import AppDriver
from tests.support.slack_driver import SlackDriver

# Load environment variables from .env file
load_dotenv()


@pytest.fixture(scope='session')
def app():
    app = AppDriver()
    try:
        app.start()
        yield app
    finally:
        app.stop()


@pytest.fixture(scope='session')
def slack():
    slack = SlackDriver()
    try:
        yield slack
    finally:
        slack.stop()
