from extractors.ktp_common import _select_field, _get_nik


def extract_from_list_of_str(lines: list):
    nik = _get_nik(lines)
    _nama = _select_field("nama", lines)

    equal_idx = 0
    try:
        equal_idx = _nama.index("=")
    except:
        pass
    semicolon_idx = 0
    try:
        semicolon_idx = _nama.index(":")
    except:
        pass

    equal_or_semicolon_idx = max(equal_idx, semicolon_idx)
    _nama = _nama[equal_or_semicolon_idx:]
    _nama_list = _nama.split(" ")
    
    _nama_list = filter(lambda s: s.isupper(), _nama_list)
    nama = " ".join(list(_nama_list))

    data = {"nik": nik, "nama": nama}
    return {"success": True, "data": data, "type": "ktp"}
