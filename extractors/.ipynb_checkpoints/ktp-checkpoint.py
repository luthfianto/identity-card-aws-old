from fuzzywuzzy import process
from typing import List


def _select_field(field: str, source: List[str]):
    field1 = process.extractOne(field, source)[0]
    field1split = field1.split(" ")
    field_word = process.extractOne(field1, field1split)[0]
    field_word_index = field1split.index(field_word)
    return " ".join(field1split[field_word_index + 1 :])


def _select_field2(field: str, source: List[str]):
    return " ".join(process.extractOne(field, source)[0].split(" ")[1:])


def _get_rtrw(source):
    rtrw = _select_field2("rtrw", source)
    return rtrw


def _get_nik(source):
    def _count(source):
        return sum(c.isdigit() for c in source)

    nik2 = process.extract("NIK", source, limit=2)
    nik2
    tuple_list = list(map(lambda el: (el, _count(el[0])), nik2))
    tuple_list

    from operator import itemgetter
    import re

    nik_string = max(tuple_list, key=itemgetter(1))[0][0]
    digit_list = re.findall("\d+", nik_string)
    return "".join(digit_list)


def _get_address(source):
    address = _select_field2("alamat", source)
    #     address = address[3:]
    return address


def extract_from_list_of_str(lines: list):
    nama = _select_field("nama", lines)
    nik = _get_nik(lines)
    address = _get_address(lines)
    rtrw = _get_rtrw(lines)
    keldesa = _select_field2("kel/desa", lines)
    kecamatan = _select_field2("kecamatan", lines)

    data = {
        "nik": nik,
        "nama": nama,
        "addresses": {
            "address": address,
            "rtrw": rtrw,
            "keldesa": keldesa,
            "kecamatan": kecamatan,
        },
    }
    return {"success": True, "data": data, "type": "ktp"}

def extract(text_detections: list):
    if not text_detections:
        return {"success": False, "data": None, "error": "NO_TEXT_DETECTED"}
    lines = [text["DetectedText"] for text in text_detections if text["Type"] == "LINE"]
    return extract_from_list_of_str(lines)
