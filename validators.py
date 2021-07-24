import re
from collections import OrderedDict
from datetime import datetime
from typing import Union

from email_validator import EmailNotValidError
from email_validator import validate_email as validate_mail


def validate_email(email_string: str) -> Union[str, bool]:
    """ validate email with email_validator
    >>> validate_email("sevenamber@gmail.com")
    'sevenamber@gmail.com'
    >>> validate_email("sevenamber2gmail.com")
    False
    >>> validate_email("seven.amber@gmail.com")
    'seven.amber@gmail.com'
    >>> validate_email("seven.amber@gmail")
    False
    """
    try:
        validate_mail(email_string, check_deliverability=False)
    except EmailNotValidError:
        return False
    else:
        return email_string


def validate_phone(phone_string: str) -> Union[str, bool]:
    """
    return phone_string as it is if it valid to: +7 xxx xxx xx xx
    >>> validate_phone("+7 123 456 78 90")
    '+7 123 456 78 90'
    >>> validate_phone("+8 123 456 78 90")
    False
    >>> validate_phone("+7(123)4567890")
    False
    >>> validate_phone("+7(123)456-78-90")
    False
    """
    pattern = r"[+]7 \d{3} \d{3} \d{2} \d{2}"
    return phone_string if re.match(pattern, phone_string) else False


def validate_date(date_string: str) -> Union[str, bool]:
    """
    return datetime obj if date has one of valid format:
    DD.MM.YYYY
    YYYY - MM - DD
    else None
    >>> validate_date("12.04.1982")
    '12.04.1982'
    >>> validate_date("1982 - 04 - 12")
    '1982 - 04 - 12'
    >>> validate_date("1982-04-12")
    False
    >>> validate_date("1982-04-31")
    False
    """
    try:
        datetime.strptime(date_string, "%d.%m.%Y").date()
    except ValueError:
        try:
            datetime.strptime(date_string, "%Y - %m - %d").date()
        except ValueError:
            pass
        else:
            return date_string
    else:
        return date_string
    return False


validators = OrderedDict({
    "date": validate_date,
    "phone": validate_phone,
    "email": validate_email,
    "text": lambda x: True,
})

if __name__ == "__main__":
    import doctest
    doctest.testmod()