import random

import requests
from tinydb import TinyDB

from config import Config

if __name__ == '__main__':
    values = {
        "date": "12.02.2015",
        "phone": "+7 012 345 67 89",
        "email": "mail@mail.ru",
        "text": "test",
    }

    url = "http://127.0.0.1:5000/get_form"

    db = TinyDB(Config.DB)
    size_db = len(db.all())

    random_doc_id = random.randint(1, size_db)
    variant = dict(db.get(doc_id=random_doc_id))
    variant.popitem()
    # variant.update({"second_email_user": "email",
    #                 "home_phone_user": "phone"})
    data = {key: values[value] for key, value in variant.items() if key != "name"}
    response = requests.post(url=url, data=data).json()
    print(response, variant.get('name'))
