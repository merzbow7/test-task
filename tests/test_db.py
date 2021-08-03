# pytest
from pathlib import Path
from random import choice, randint

import pytest
import requests
from tinydb import TinyDB

from config import Config
from utils import typing_request


class TestClass:

    @pytest.fixture(autouse=True)
    def initialized_tasks_db(self, count_tests):
        """Connect to db before testing, disconnect after."""
        self.count_tests = count_tests
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
        """get test self.db replace types random values same types and test itself"""
        size_db = len(self.db.all())

        for _ in range(self.count_tests):
            variant = dict(self.db.get(doc_id=randint(1, size_db)))
            test_data = {key: self.test_types[value]() for key, value in variant.items() if key != "name"}

            req = requests.post(self.url, data=test_data)
            assert variant["name"] == req.json()

    @pytest.mark.smoke
    def test_empty_post(self):
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
            variant = dict(self.db.get(doc_id=randint(1, size_db)))
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
            variant = dict(self.db.get(doc_id=randint(1, size_db)))

            variant.update({"second_email_user": "email",
                            "home_phone_user": "phone"})

            data = {key: self.test_types[value]() for key, value in variant.items() if key != "name"}

            response = requests.post(self.url, data=data).json()
            assert response == variant.get('name')
