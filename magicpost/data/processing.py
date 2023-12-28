import json
import random
from datetime import date, timedelta
from pathlib import Path
from typing import List

from unidecode import unidecode
from vietnam_provinces import District, Province
from vietnam_provinces.enums import DistrictEnum, ProvinceEnum
from vietnam_provinces.enums.wards import WardEnum
from zipcode import ZipcodeEnum

module_directory = Path(__file__).resolve().parent
data_path = module_directory / "uit_member.json"


def load_json(path: str):
    with open(path, "r") as f:
        return json.load(f)


def process_fullnames():
    names_data = load_json(data_path)

    fullnames = map(lambda x: x["full_name"], names_data)

    with open(module_directory / "fullnames.json", "w") as f:
        json.dump(list(fullnames), f, ensure_ascii=False)


def load_ward_to_zipcode():
    ward_to_zipcode = {}

    for zipcode in ZipcodeEnum:
        w = zipcode.value.value
        ward_to_zipcode[w.code] = zipcode.name.replace("Z_", "")

    return ward_to_zipcode


def process_phones():
    phones_data = load_json(module_directory / "phones.json")

    cleaned_phones = []
    for phone in phones_data:
        tmp = phone["PhoneNumber"]
        tmp = tmp.replace("+84", "0").replace("-", "")
        cleaned_phones.append(tmp)

    with open(module_directory / "phones-cleaned.json", "w") as f:
        json.dump(cleaned_phones, f, ensure_ascii=False)


def create_hubs():
    hubs = []
    phones_data: List[str] = load_json(module_directory / "phones-cleaned.json")
    ward2zipcode = load_ward_to_zipcode()

    for province_enum in ProvinceEnum:
        province = province_enum.value
        district = random.choice(
            list(
                d.value for d in DistrictEnum if d.value.province_code == province.code
            )
        )
        ward = random.choice(
            list(w.value for w in WardEnum if w.value.district_code == district.code)
        )
        hub_name = f"Điểm tập kết {province.name}"
        address = f"{ward.name}, {district.name}, {province.name}"
        phone = random.choice(list(phones_data))
        zipcode = ward2zipcode.get(ward.code, "10000")
        hub = {
            "name": hub_name,
            "address": address,
            "phone": phone,
            "zipcode": zipcode,
            "offices": [],
        }

        office_num = 5
        wards = random.sample(
            list(w.value for w in WardEnum if w.value.district_code == district.code),
            office_num,
        )
        for w in wards:
            office_name = f"Điểm giao dịch {w.name}"
            address = f"{w.name}, {district.name}, {province.name}"
            phone = random.choice(list(phones_data))
            zipcode = ward2zipcode.get(w.code, "33707")

            office = {
                "name": office_name,
                "address": address,
                "phone": phone,
                "zipcode": zipcode,
            }

            hub["offices"].append(office)

        hubs.append(hub)

    with open(module_directory / "hubs.json", "w") as f:
        json.dump(hubs, f, ensure_ascii=False)

    return hubs


def transform_to_username(full_name):
    # Remove accents using ASCII folding
    folded_name = unidecode(full_name)

    # Split the folded name into individual words
    words = folded_name.split()

    # Concatenate the words, convert to lowercase, and remove spaces
    username = "".join(words).lower()

    return username


def random_date(start_year, end_year):
    start_date = date(start_year, 1, 1)
    end_date = date(end_year + 1, 1, 1) - timedelta(days=1)

    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)

    return random_date


def create_users():
    phones_data: List[str] = load_json(module_directory / "phones-cleaned.json")
    names_data: List[str] = load_json(module_directory / "fullnames.json")

    users = []
    usernames = set()

    for _ in range(3000):
        fullname = random.choice(names_data)
        phone = random.choice(phones_data)
        username = transform_to_username(fullname)
        birth = random_date(1970, 2000)

        user = {
            "username": username,
            "fullname": fullname,
            "phone": phone,
            "birth": birth.strftime("%Y-%m-%d"),
        }

        if username in usernames:
            continue

        usernames.add(username)

        users.append(user)

    with open(module_directory / "users.json", "w") as f:
        json.dump(users, f, ensure_ascii=False)


if __name__ == "__main__":
    # process_fullnames()
    # process_phones()
    # create_hubs()
    create_users()
    # print(load_ward_to_zipcode())
    pass
