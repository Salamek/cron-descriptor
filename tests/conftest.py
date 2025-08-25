import pytest

from cron_descriptor import Options


@pytest.fixture
def options() -> Options:
    options = Options()
    options.locale_code = "en_US"
    return options
