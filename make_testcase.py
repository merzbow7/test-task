from collections import OrderedDict
from functools import partial
from itertools import combinations
from random import choice, randint

from tinydb import TinyDB, Query

from config import Config


def make_test_db(*, min_count_entries: int = None, db_name: str = None) -> None:
    if not db_name:
        db = TinyDB('test_db.json')
    else:
        db = TinyDB(db_name)
    if not min_count_entries:
        min_count_entries = 5000

    field = ('email', 'phone', 'date', 'text')
    field_fnc = partial(combinations, field)
    tests = ("abstract", "order", "user", "lead", "random", "secret",
             "special", "simple", "serial", "personal", "real")

    counts = 0
    while counts < min_count_entries:
        test_case = []

        for i in reversed(range(2, 5)):
            for variant in field_fnc(i):
                form_dict = {f"{value}_{choice(tests)}": value for value in variant}

                if db.search(Query().fragment(form_dict)):
                    continue

                base_form = OrderedDict(
                    {"name": f"{choice(tests)} form with {choice(variant)} {randint(11111, 99999)}"})
                base_form.update(form_dict)
                test_case.append(base_form)

        counts += len(test_case)

        if len(test_case):
            db.insert_multiple(test_case)


if __name__ == '__main__':
    make_test_db(db_name=Config.DB, min_count_entries=1000)
