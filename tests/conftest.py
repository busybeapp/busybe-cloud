import os
import pytest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@pytest.fixture(scope="session", autouse=True)
def set_env_for_testing():
    os.environ["ENV"] = "testing"
    load_dotenv(override=True)

    yield

    del os.environ["ENV"]
    load_dotenv(override=True)
