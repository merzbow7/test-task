import pytest

from validators import *


@pytest.fixture()
def valid_emails():
    """ valid emails """

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
    """ invalid emails """
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
    """ valid phones """
    return (
        "+7 012 345 67 89 ",
        "+7 123 456 78 90 ",
    )


@pytest.fixture()
def invalid_phones():
    """ invalid phones """
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
    """ valid date """
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
    """ invalid date """
    return (
        "31.04.1992",
        "29.02.2021",
        "01.13.2001",
        "202 - 07 - 01",
        "2021 - 15 - 15",
        "1999 - 00 - 01",
    )


@pytest.mark.valid
def test_email_validator(valid_emails, invalid_emails):
    for email in valid_emails:
        assert validate_email(email)

    for email in invalid_emails:
        assert not validate_email(email)


@pytest.mark.valid
def test_phone_validator(valid_phones, invalid_phones):
    for phone in valid_phones:
        assert validate_phone(phone)

    for phone in invalid_phones:
        assert not validate_phone(phone)


@pytest.mark.valid
def test_date_validator(valid_date, invalid_date):
    for date in valid_date:
        assert validate_date(date)

    for date in invalid_date:
        assert not validate_date(date)
