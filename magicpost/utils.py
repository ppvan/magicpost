def is_hub(zipcode: str):
    if zipcode.endswith("000"):
        return True
    return False
