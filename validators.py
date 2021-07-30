import re
from collections import OrderedDict
from datetime import datetime
from typing import Union

from email_validator import EmailNotValidError
from email_validator import validate_email as validate_mail


def validate_email(email_string: str) -> Union[str, bool]:
    try:
        validate_mail(email_string, check_deliverability=False)
        return email_string
    except EmailNotValidError:
        return False


def validate_phone(phone_string: str) -> Union[str, bool]:
    pattern = r"[+]7 \d{3} \d{3} \d{2} \d{2}"
    return phone_string if re.match(pattern, phone_string) else False


def validate_date(date_string: str) -> Union[str, bool]:
    try:
        datetime.strptime(date_string, "%d.%m.%Y")
        return date_string
    except ValueError:
        try:
            datetime.strptime(date_string, "%Y - %m - %d")
            return date_string
        except ValueError:
            return False


validators = OrderedDict({
    "date": validate_date,
    "phone": validate_phone,
    "email": validate_email,
    "text": lambda x: True,
})
