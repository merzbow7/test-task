# pytest
from pathlib import Path
from random import choice, randint

import pytest
import requests
from tinydb import TinyDB

from config import Config
from utils import typing_request
from validators import *


class TestClass:

    @pytest.fixture(autouse=True)
    def initialized_tasks_db(self):
        """Connect to db before testing, disconnect after."""
        self.count_tests = 500

        self.path_db = Path(__file__).parent.parent / Config.DB
        self.db = TinyDB(self.path_db)
        self.url = 'http://127.0.0.1:5000/get_form'

        self.test_types = {
            "text": lambda: choice(("test", "dsoifus9", "тест")),
            "phone": lambda: choice(("+7 123 456 78 90", "+7 012 345 67 89", "+7 111 111 11 11")),
            "email": lambda: choice(("test@test.ru", "root@root.dev", "ya@ya.ya")),
            "date": lambda: choice(("1986 - 04 - 22", "1.01.2021")),
        }

        yield  # testing

        # Teardown : stop db
        self.db.close()

    def test_self_is_self(self):
        """
        get test self.db replace types random values same types and test itself
        """
        size_db = len(self.db.all())

        for _ in range(self.count_tests):
            variant = dict(self.db.get(doc_id=randint(0, size_db)))
            test_data = {key: self.test_types[value]() for key, value in variant.items() if key != "name"}

            req = requests.post(self.url, data=test_data)
            assert variant["name"] == req.json()

    @pytest.mark.smoke
    def test_empy_post(self):
        test_data = {}
        req = requests.post(self.url, data=test_data).json()
        assert {} == req

    @pytest.mark.smoke
    def test_repeat_data(self):
        test_data = {"email_secret": "email@email.ru", "email_secret2": "email@email.ru",
                     "email_secret3": "email@email.ru"}
        req = requests.post(self.url, data=test_data).json()
        assert req == {"email_secret": "email", "email_secret2": "email", "email_secret3": "email"}

    def test_some_not_valid_data(self):
        size_db = len(self.db.all())
        for _ in range(self.count_tests):
            variant = dict(self.db.get(doc_id=randint(0, size_db)))
            variant.pop("name")
            for key, value in variant.items():
                variant[key] = self.test_types[value]()
            typed_data = typing_request(variant)
            for key, value in variant.items():
                if "email" in key:
                    variant[key] = "wrong_mail@mail@com"

            response = requests.post(self.url, data=variant).json()
            assert response != typed_data

    def test_some_updated_random_data_from_db(self):

        size_db = len(self.db.all())
        for _ in range(self.count_tests):
            variant = dict(self.db.get(doc_id=randint(0, size_db)))

            variant.update({"second_email_user": "email",
                            "home_phone_user": "phone"})

            data = {key: self.test_types[value]() for key, value in variant.items() if key != "name"}

            response = requests.post(self.url, data=data).json()
            assert response == variant.get('name')


class TestValidators:

    @pytest.mark.valid
    def test_email_validator(self):
        valid_emails = (
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
        for email in valid_emails:
            assert validate_email(email)

        invalid_emails = (
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
        for email in invalid_emails:
            assert not validate_email(email)

    @pytest.mark.valid
    def test_phone_validator(self):
        valid_phones = (
            "+7 012 345 67 89 ",
            "+7 123 456 78 90 ",
        )
        for phone in valid_phones:
            assert validate_phone(phone)

        invalid_phones = (
            "7 123 456 78 90",
            "8 123 456 78 90",
            "+8 123 456 78 90",
            "+7(123)4567890",
            "+7-123-456-78-90",
            "+7 (123) 456-78-90",
            "8 (123) 456-78-90",
        )
        for phone in invalid_phones:
            assert not validate_phone(phone)

    @pytest.mark.valid
    def test_date_validator(self):
        "%d.%m.%Y"
        "%Y - %m - %d"
        valid_date = (
            "30.04.1992",
            "31.12.1999",
            "01.01.2001",
            "2020 - 07 - 01",
            "2021 - 12 - 31",
            "1999 - 01 - 01",
        )
        for date in valid_date:
            assert validate_date(date)

        invalid_date = (
            "31.04.1992",
            "29.02.2021",
            "01.13.2001",
            "202 - 07 - 01",
            "2021 - 15 - 15",
            "1999 - 00 - 01",
        )
        for date in invalid_date:
            assert not validate_date(date)
