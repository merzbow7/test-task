import os
from pathlib import Path

import pytest
from tinydb import TinyDB

from config import Config


def pytest_report_header():
    """ test header """
    return f"launch on '{os.uname().nodename}'"


def pytest_addoption(parser):
    parser.addoption("--count", action="store", help="count of cycles in tests")


@pytest.fixture()
def count_tests(pytestconfig):
    """ read count of cycles in tests from cli """
    try:
        count = pytestconfig.getoption('count')
        if not count or int(count) < 1:
            raise ValueError
        return int(count)

    except ValueError:
        return 100


@pytest.fixture()
def initialized_db():
    """Connect to db before testing, disconnect after."""

    path_db = Path(__file__).parent.parent / Config.DB
    db = TinyDB(path_db)

    yield db

    db.close()
