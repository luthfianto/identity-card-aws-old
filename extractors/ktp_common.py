from fuzzywuzzy import process
from typing import List


def _select_field(field: str, source: List[str]):
    field1 = process.extractOne(field, source)[0]
    field1split = field1.split(" ")
    field_word = process.extractOne(field1, field1split)[0]
    field_word_index = field1split.index(field_word)

    return " ".join(field1split[field_word_index + 1 :])


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
    if digit_list:
        return "".join(digit_list)
    
    backup = " ".join(source[:5])
    backup2 = re.findall("\d+", backup)
    return "".join(backup2)
