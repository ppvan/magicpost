from typing import List

from fastapi import APIRouter
from vietnam_provinces import District, Province
from vietnam_provinces.enums import DistrictEnum, ProvinceEnum
from vietnam_provinces.enums.wards import Ward, WardEnum

router = APIRouter(prefix="/address", tags=["Wards"])


@router.get("/p/", response_model=List[Province])
def get_provices():
    return [e.value for e in ProvinceEnum]


@router.get("/p/{p_code}", response_model=Province)
def get_provice(p_code: int):
    return ProvinceEnum[f"P_{p_code}"].value


@router.get("/p/{p_code}/districts/", response_model=List[District])
def get_provice_districts(p_code: int):
    return [e.value for e in DistrictEnum if e.province_code == p_code]


@router.get("/d/", response_model=List[District])
def get_districts():
    return [e.value for e in DistrictEnum]


@router.get("/d/{d_code}", response_model=District)
def get_district(d_code: int):
    return DistrictEnum[f"D_{d_code}"].value


@router.get("/d/{d_code}/wards/", response_model=List[Ward])
def get_district_wards(d_code: int):
    return [e.value for e in WardEnum if e.district_code == d_code]


# @router.get("/z/", response_model=List[Ward])
# def get_ward_with_zipcode():
#     return [e.value for e in WardEnum]
