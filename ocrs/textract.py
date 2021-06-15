from typing import List


def ismixed(s):
    return any(c.islower() for c in s) and any(c.isupper() for c in s)


JUDUL_JUGA = ["NIK", "IK", "PROVINSI", "KABUPATEN", "RTRW", "RT/RW", "RTW", "RTIRW", "RT RW", "VIK", "A"]


def textract_lines_to_rekognition(lines: List[str]):
    alll = []
    segment = []
    for word in lines:
        if ismixed(word) or word in JUDUL_JUGA:
            alll.append(" ".join(segment))
            segment = []
        segment.append(word)
    return alll
