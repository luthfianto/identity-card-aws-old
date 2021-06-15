from ocrs.textract import ismixed
from fuzzywuzzy import process
from typing import Any, Dict, List
from extractors.ktp_common import _select_field, _get_nik
from extractors.common import sanitize, ERROR_COULD_NOT_EXTRACT_TEXT
import re

RE_BIRTHDAY = re.compile("[A-Z]{2,}|[\d-]+")
RE_D = re.compile("\d")
RE_RTRW = re.compile("[\d/\?]+")


def _select_field2(field: str, source: List[str]):
    return " ".join(process.extractOne(field, source)[0].split(" ")[1:])


def _get_rtrw(source: List[str]):
    rtrw = _select_field2("RT/RW", source)
    matches = RE_RTRW.findall(rtrw)
    res = "".join(matches)
    if res.isdigit():
        if len(res) == 6:
            return res[:3] + "/" + res[3:]
        if len(res) == 7:
            if res[3] in [1, 2, 7]:
                return res[:3] + "/" + res[4:]
    return res


def _get_address(source: List[str]):
    address = _select_field2("alamat", source)
    return address


def _get_birthday_date(birthday_str_raw: str):
    i = 0
    j = 0
    for char in birthday_str_raw[::-1]:
        i += 1
        if char.isdigit():
            j += 1
        # Should at least have 8 digits
        if j >= 8:
            res = birthday_str_raw[-i:]
            return res
    return birthday_str_raw


def _has_digit(string: str):
    return RE_D.search(string)


def _get_birthday_place_date(birthdaystr: str):
    birthday_list = re.findall(RE_BIRTHDAY, birthdaystr)

    birthday_place = " ".join(filter(lambda x: x.isupper(), birthday_list))
    birthday_date_1 = list(filter(_has_digit, birthday_list))
    birthday_date_2 = " ".join(birthday_date_1)
    birthday_date = _get_birthday_date(birthday_date_2)

    birthday_place = birthday_place.replace("PEREMPUAN", "")

    return (birthday_place, birthday_date)


def _get_name(lines: List[str]):
    lines_ = list(map(lambda x: " ".join(filter(ismixed, x.split(" "))), lines))
    Nama = process.extractOne("Nama", lines_)[0]
    nama_idx = lines_.index(Nama)
    nama_ = lines[nama_idx]
    nama_ = " ".join(filter(lambda s: s.isupper(), nama_.split(" ")))
    if nama_:
        return nama_.replace(":", "")
    try:
        name_str = lines[nama_idx + 1]
        return name_str.replace(":", "")
    except Exception as e:
        return ""


def extract_from_list_of_str(lines: List[str]):
    if not lines:
        return {"success": False, "data": None, "error": ["NO_TEXT_DETECTED"]}
    nama = sanitize(_get_name(lines))
    nik = _get_nik(lines)
    if nama == "" and (len(nik) < 14 or len(nik) > 20):
        return {
            "success": False,
            "data": None,
            "errors": [ERROR_COULD_NOT_EXTRACT_TEXT],
        }

    address = sanitize(_get_address(lines))
    rtrw = _get_rtrw(lines)
    keldesa = sanitize(_select_field2("Kel/Desa", lines))
    kecamatan = sanitize(_select_field2("Kecamatan", lines))
    birthday_place, birthday_date = _get_birthday_place_date(
        _select_field2("Tempat/Tgl Lahir", lines)
    )

    data = {
        "nik": nik,
        "name": nama,
        "birthday": {"place": sanitize(birthday_place), "date": birthday_date},
        "addresses": {
            "address": address,
            "rtrw": rtrw,
            "keldesa": keldesa,
            "kecamatan": kecamatan,
        },
    }

    return {"success": True, "data": data, "type": "ktp"}


def extract(text_detections: List[Dict[str, str]]):
    if not text_detections:
        return {"success": False, "data": None, "error": ["NO_TEXT_DETECTED"]}
    lines = [text["DetectedText"] for text in text_detections if text["Type"] == "LINE"]
    return extract_from_list_of_str(lines)
