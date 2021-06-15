from typing import Dict, List
from fuzzywuzzy import process
from operator import itemgetter
import re
from extractors.npwp_common import _get_raw_nomor, _get_nomor_and_index

RE_D = re.compile('\d')
def _has_digit(string):
    return RE_D.search(string)

def _get_address(source: List[str], start_index: int):
    addresses_candidate = source[start_index:]
    address_lines = [addresses_candidate[0]]
    
    for address_line in addresses_candidate[1:]:
        if _has_digit(address_line):
            break
        address_lines.append(address_line)
    
    return address_lines

def extract(text_detections: List[dict]):
    if not text_detections:
        return {"success": False, "data": None, "error": ["NO_TEXT_DETECTED"]}

    lines = [text["DetectedText"] for text in text_detections if text["Type"] == "LINE"]

    nomor_str, nomor_index = _get_nomor_and_index(lines, "NPWP")
    
    try:
        nama = lines[nomor_index+1]
        address = _get_address(lines, nomor_index+2)
    except Exception as e:
        return {'success': False, 'data': None, 'errors': ['FAILED_TO_EXTRACT']}
    
    data = {"npwp": nomor_str, "name": nama, "addresses": address}
    return {"success": True, "data": data, "type": "npwp"}
