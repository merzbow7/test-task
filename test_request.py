import requests
from tinydb import TinyDB

from make_testcase import make_test_db

if __name__ == '__main__':
    values = {
        "date": "12.02.2015",
        "phone": "+7 012 345 67 89",
        "email": "mail@mail.ru",
        "text": "test",
    }

    url = "http://127.0.0.1:5000/get_form"
    test_db = "test.json"
    make_test_db(db_name=test_db, min_count_entries=100)
    db = TinyDB(test_db)
    for item in db:
        data = {key: values[value] for key, value in item.items() if key != "name"}
        response = requests.post(url=url, data=data).json()
        print(response)
