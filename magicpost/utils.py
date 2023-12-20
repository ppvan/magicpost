from typing import List


def is_hub(zipcode: str):
    if zipcode.endswith("000"):
        return True
    return False


def is_valid_zipcode(zipcode: str):
    if len(zipcode) != 5:
        return False

    try:
        return True
    except AttributeError:
        return False


def find_next(lst: List[str], item: str):
    try:
        index_of_key = lst.index(item)
        if index_of_key < len(lst) - 1:
            return lst[index_of_key + 1]
        else:
            return None
    except ValueError:
        return None
