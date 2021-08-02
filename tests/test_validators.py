import pytest

from validators import *


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
