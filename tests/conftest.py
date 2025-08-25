import pytest

from cron_descriptor import Options


@pytest.fixture
def options() -> Options:
    return Options(locale_code="en_US")
