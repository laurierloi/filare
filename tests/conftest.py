from tests.fixtures.models import *  # noqa: F401,F403


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")
