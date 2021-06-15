from extractors.ktp import _select_field, _get_nik

def extract_from_list_of_str(lines: list):
    _nama = _select_field("nama", lines).split(" ")
    _nama = filter(lambda s: s.isupper(), _nama)
    _nama = filter(lambda s: '=' not in s, _nama)
    nama = " ".join(list(_nama))
    nik = _get_nik(lines)

    data = {
        "nik": nik,
        "nama": nama,
    }
    return {"success": True, "data": data, "type": "ktp"}