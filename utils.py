from itertools import combinations
from typing import Union, List

from tinydb import TinyDB, Query

from validators import validators


def typing_request(data: dict) -> dict:
    """
    validate and set type for all field in data
    """
    result = {}
    for name, field in data.items():
        for type_, validator in validators.items():
            if validator(field):
                result[name] = type_
                break
    return result


def make_combinations_from_data(typed_data: dict) -> List[dict]:
    """
    Return successive combinations (from 1  to  len(data)) length of elements in the data.
    """
    result = []
    for i in range(len(typed_data), 0, -1):
        for item in combinations(typed_data.items(), i):
            result.append(dict(item))
    return result


def find_form_for_request(data: dict, db: TinyDB) -> Union[str, dict]:
    """
    sequential search all combination from variants(data) in db,
    and returned form name on success
    """
    typed_request = typing_request(data)
    data_set = set(typed_request.items())
    variants = make_combinations_from_data(typed_request)

    Entry = Query()
    for variant in variants:
        entries = db.search(Entry.fragment(variant))
        for entry in entries:
            entry_ = {key: value for key, value in entry.items() if key != "name"}
            entry_name = entry.get('name')
            entry_set = set(entry_.items())
            if entry_set.issubset(data_set):
                return entry_name
    return typing_request(data)
