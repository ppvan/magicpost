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
