from typing import List
from extractors.npwp_common import _get_raw_nomor, _get_nomor_and_index


def extract_from_list_of_str(lines: List[str]):
    if not lines:
        return {"success": False, "data": None, "error": "NO_TEXT_DETECTED"}

    nomor_str, nomor_index = _get_nomor_and_index(lines, "NPWP")
    _nama = lines[nomor_index + 1].split()
    _nama = filter(lambda s: s.isupper(), _nama)
    nama = " ".join(_nama)


    data = {"npwp": nomor_str, "name": nama}
    return {"success": True, "data": data, "type": "npwp"}

