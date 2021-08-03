# pytest
from random import choice, randint

import pytest
import requests

from utils import typing_request

test_types = {
    "text": lambda: choice(("test", "dsoifus9", "тест")),
    "phone": lambda: choice(("+7 123 456 78 90", "+7 012 345 67 89", "+7 111 111 11 11")),
    "email": lambda: choice(("test@test.ru", "root@root.dev", "ya@ya.ya")),
    "date": lambda: choice(("1986 - 04 - 22", "1.01.2021")),
}

url = 'http://127.0.0.1:5000/get_form'


def test_self_is_self(initialized_db, count_tests):
    """
    get test db replace types random values same types and test itself
    """
    db = initialized_db
    size_db = len(db.all())

    for _ in range(count_tests):
        variant = dict(db.get(doc_id=randint(1, size_db)))
        test_data = {key: test_types[value]() for key, value in variant.items() if key != "name"}

        req = requests.post(url, data=test_data)
        assert variant["name"] == req.json()


@pytest.mark.smoke
def test_empty_post():
    test_data = {}
    req = requests.post(url, data=test_data).json()
    assert {} == req


@pytest.mark.smoke
def test_repeat_data():
    test_data = {"email_secret": "email@email.ru", "email_secret2": "email@email.ru",
                 "email_secret3": "email@email.ru"}
    req = requests.post(url, data=test_data).json()
    assert req == {"email_secret": "email", "email_secret2": "email", "email_secret3": "email"}


def test_some_not_valid_data(initialized_db, count_tests):
    db = initialized_db
    size_db = len(db.all())

    for _ in range(count_tests):
        variant = dict(db.get(doc_id=randint(1, size_db)))
        variant.pop("name")

        for key, value in variant.items():
            variant[key] = test_types[value]()
        typed_data = typing_request(variant)

        for key, value in variant.items():
            if "email" in key:
                variant[key] = "wrong_mail@mail@com"

        response = requests.post(url, data=variant).json()
        assert response != typed_data


def test_some_updated_random_data_from_db(initialized_db, count_tests):
    db = initialized_db
    size_db = len(db.all())
    for _ in range(count_tests):
        variant = dict(db.get(doc_id=randint(1, size_db)))
        variant.update({"second_email_user": "email",
                        "home_phone_user": "phone"})
        data = {key: test_types[value]() for key, value in variant.items() if key != "name"}
        response = requests.post(url, data=data).json()
        assert response == variant.get('name')
