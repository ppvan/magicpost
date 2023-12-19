from typing import List

from fastapi import APIRouter, Depends
from vietnam_provinces import District, Province
from vietnam_provinces.enums import DistrictEnum, ProvinceEnum
from vietnam_provinces.enums.wards import Ward, WardEnum

from magicpost.address.exceptions import DistrictNotFound, ProvinceNotFound

router = APIRouter(prefix="/address", tags=["Wards"])


def valid_provice_code(p_code: int) -> Province:
    try:
        return ProvinceEnum[f"P_{p_code}"].value
    except KeyError:
        raise ProvinceNotFound()


def valid_district_code(d_code: int) -> District:
    try:
        return DistrictEnum[f"D_{d_code}"].value
    except KeyError:
        raise DistrictNotFound()


@router.get("/p/", response_model=List[Province])
def get_provices():
    return [e.value for e in ProvinceEnum]


@router.get("/p/{p_code}", response_model=Province)
def get_provice(province: Province = Depends(valid_provice_code)):
    return province


@router.get("/p/{p_code}/districts/", response_model=List[District])
def get_provice_districts(province: Province = Depends(valid_provice_code)):
    return [e.value for e in DistrictEnum if e.province_code == province.code]


@router.get("/d/", response_model=List[District])
def get_districts():
    return [e.value for e in DistrictEnum]


@router.get("/d/{d_code}", response_model=District)
def get_district(district: District = Depends(valid_district_code)):
    return district


@router.get("/d/{d_code}/wards/", response_model=List[Ward])
def get_district_wards(district: District = Depends(valid_district_code)):
    return [e.value for e in WardEnum if e.district_code == district.code]


# @router.get("/z/", response_model=List[Ward])
# def get_ward_with_zipcode():
#     return [e.value for e in WardEnum]
