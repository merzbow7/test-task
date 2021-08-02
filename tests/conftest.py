from pathlib import Path

import pytest
from tinydb import TinyDB

from config import Config


@pytest.fixture()
def initialized_db():
    """Connect to db before testing, disconnect after."""

    path_db = Path(__file__).parent.parent / Config.DB
    db = TinyDB(path_db)

    yield db

    db.close()


@pytest.fixture()
def valid_emails():
    return (
        'email@example.com',
        'firstname.lastname@example.com',
        'email@subdomain.example.com',
        'firstname+lastname@example.com',
        'firstname^lastname@example.com',
        'firstname%lastname@example.com',
        'firstname%lastname@example.com',
        '1234567890@example.com',
        'email@example-one.com',
        '_______@example.com',
        'email@example.name',
        'email@example.museum',
        'email@example.co.jp',
        'firstname-lastname@example.com',
    )


@pytest.fixture()
def invalid_emails():
    return (
        '#@%^%#$@#$@#.com',
        '@example.com',
        'Joe Smith <email@example.com>',
        'email.example.com',
        'email@example@example.com',
        '.email@example.com',
        'email.@example.com',
        'email..email@example.com',
        'email@example.com (Joe Smith)',
        'email@example',
        'email@-example.com',
        'email@111.222.333.44444',
        'email@example..com',
        'Abc..123@example.com',
    )


@pytest.fixture()
def valid_phones():
    return (
        "+7 012 345 67 89 ",
        "+7 123 456 78 90 ",
    )


@pytest.fixture()
def invalid_phones():
    return (
        "7 123 456 78 90",
        "8 123 456 78 90",
        "+8 123 456 78 90",
        "+7(123)4567890",
        "+7-123-456-78-90",
        "+7 (123) 456-78-90",
        "8 (123) 456-78-90",
    )


@pytest.fixture()
def valid_date():
    return (
        "30.04.1992",
        "31.12.1999",
        "01.01.2001",
        "2020 - 07 - 01",
        "2021 - 12 - 31",
        "1999 - 01 - 01",
    )


@pytest.fixture()
def invalid_date():
    return (
        "31.04.1992",
        "29.02.2021",
        "01.13.2001",
        "202 - 07 - 01",
        "2021 - 15 - 15",
        "1999 - 00 - 01",
    )
