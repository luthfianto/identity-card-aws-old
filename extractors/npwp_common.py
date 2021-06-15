from typing import Dict, List
from fuzzywuzzy import process
from operator import itemgetter
import re

RE_D = re.compile("\d")
RE_D_DASH_DOT = re.compile("[\d\.-]+")


def _get_raw_nomor(source: List[str], guide: str):
    def _count_number_of_digits(source: str):
        return sum(c.isdigit() for c in source)

    nomor_candidates = process.extract(guide, source, limit=2)
    digit_count_tuple_list = list(
        map(lambda el: (el, _count_number_of_digits(el[0])), nomor_candidates)
    )

    raw_nik_string = max(digit_count_tuple_list, key=itemgetter(1))[0][0]
    return raw_nik_string


def _get_nomor_and_index(source: List[str], guide: str) -> (str, int):
    raw_nik_string = _get_raw_nomor(source, guide)
    digit_list = re.findall(RE_D_DASH_DOT, raw_nik_string)
    nomor_string = "".join(digit_list)
    nomor_index = source.index(raw_nik_string)

    return nomor_string, nomor_index


def _has_digit(string):
    return RE_D.search(string)
