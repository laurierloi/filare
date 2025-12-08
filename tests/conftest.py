from pathlib import Path

import pytest

from tests.fixtures.models import *  # noqa: F401,F403

# Directories treated as functional/integration suites.
FUNCTIONAL_ROOTS = [
    Path(__file__).parent / "functional",
    Path(__file__).parent / "documentation",
]


def pytest_addoption(parser):
    parser.addoption(
        "--include-functional",
        action="store_true",
        default=False,
        help="Run functional/documentation tests (skipped by default).",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line(
        "markers", "functional: slow functional/integration tests (>10s)"
    )
    config.addinivalue_line("markers", "unit: fast unit tests")


def pytest_collection_modifyitems(config, items):
    include_functional = config.getoption("--include-functional")
    markexpr = (config.option.markexpr or "").lower()
    explicit_functional = include_functional or (
        "functional" in markexpr and "not functional" not in markexpr
    )
    for item in items:
        path = Path(item.fspath)
        has_functional_marker = item.get_closest_marker("functional") is not None
        is_functional_path = any(root in path.parents for root in FUNCTIONAL_ROOTS)
        is_functional = has_functional_marker or is_functional_path
        if is_functional:
            item.add_marker(pytest.mark.functional)
            if not explicit_functional:
                item.add_marker(
                    pytest.mark.skip(
                        reason="Functional tests are skipped by default; run with -m functional or --include-functional"
                    )
                )
        else:
            item.add_marker(pytest.mark.unit)
