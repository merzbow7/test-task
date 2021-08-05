# pytest
import math
from random import choice, randint
from string import ascii_lowercase

import pytest
import requests

from utils import typing_request, make_combinations_from_data, find_form_for_request

test_types = {
    "text": lambda: choice(("test", "dsoifus9", "тест")),
    "phone": lambda: choice(("+7 123 456 78 90", "+7 012 345 67 89", "+7 111 111 11 11")),
    "email": lambda: choice(("test@test.ru", "root@root.dev", "ya@ya.ya")),
    "date": lambda: choice(("1986 - 04 - 22", "1.01.2021")),
}

url = 'http://127.0.0.1:5000/get_form'


def make_data(variant: dict) -> dict:
    return {key: test_types[value]() for key, value in variant.items() if key != "name"}


def test_self_is_self(initialized_db, count_tests):
    """
    get test db replace types random values same types and test itself
    """
    db = initialized_db
    size_db = len(db.all())

    for _ in range(count_tests):
        variant = dict(db.get(doc_id=randint(1, size_db)))
        test_data = make_data(variant)

        assert variant["name"] == find_form_for_request(test_data, db)


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

        assert find_form_for_request(typed_data, db) != typed_data


def test_some_updated_random_data_from_db(initialized_db, count_tests):
    db = initialized_db
    size_db = len(db.all())
    for _ in range(count_tests):
        variant = dict(db.get(doc_id=randint(1, size_db)))
        variant.update({"second_email_user": "email",
                        "home_phone_user": "phone"})

        data = make_data(variant)
        assert find_form_for_request(data, db) == variant.get('name')


def test_combinations_count(count_tests):
    for _ in range(count_tests):
        len_dict = randint(0, 18)
        combinations = 0
        for i in range(len_dict, 0, -1):
            combinations += math.comb(len_dict, i)
        test_dict = {char: index for index, char in enumerate(ascii_lowercase[:len_dict])}
        variants = len(make_combinations_from_data(test_dict))
        assert variants == combinations


def test_combinations_once():
    data = {'a': 0, 'b': 1, 'c': 2}
    expect = [
        {'a': 0, 'b': 1, 'c': 2},
        {'a': 0, 'b': 1}, {'a': 0, 'c': 2}, {'b': 1, 'c': 2},
        {'a': 0}, {'b': 1}, {'c': 2}
    ]
    assert expect == make_combinations_from_data(data)
