"""
Limitations:
- identity cards should not be rotated/misoriented
- because identity cards are not rotated/misoriented, we can:
   - treat each lines as lines of string
   - exploit the structures of KTP/NPWP (npwp name is below npwp number, etc)
"""

from typing import Dict, Awaitable, List
from extractors import ktp, npwp, ktp_tesseract, npwp_tesseract
from tesseract_adapters import via_subprocess
import time
import boto3
import requests
import urllib.request

rekognition_client = boto3.client("rekognition", region_name="ap-southeast-1")
textract_client = boto3.client("textract", region_name="ap-southeast-1")


def _get_image_bytes_from_url(url: str) -> bytes:
    """Get bytes of JPG from URL"""
    res = requests.get(url, stream=True)
    return res.content


def _get_textract_from_image_bytes(Bytes: bytes) -> List[dict]:
    response = textract_client.detect_document_text(Document={"Bytes": Bytes})
    return response


def _get_rekog_from_image_bytes(Bytes: bytes) -> List[dict]:
    rekognition_res = rekognition_client.detect_text(Image={"Bytes": Bytes})
    return rekognition_res["TextDetections"]


def _localize_ktp_from_image_bytes(Bytes: bytes):
    return True


def _is_image_clear(Bytes: bytes):
    return True


def _is_image_clear2(bytes_: bytes):
    localizeds = _localize_ktp_from_image_bytes(bytes_)
    if not localizeds:
        return {"success": False, "data": None, "error": ["INVALID_IDENTITY_CARD"]}

    if not _is_image_clear(bytes_):
        return {"success": False, "data": None, "error": ["BLURRY_IMAGE"]}

    return {"success": True}


def main(url, type_, base64_):
    if url:
        url = url.strip()

    import base64

    # global bytes_
    bytes_ = None
    if base64_:
        # print(base64_[0:10])
        bytes_ = base64.b64decode(base64_)
        # print(bytes_[0:10])

    unique_id = int(time.time())

    if type_ == "ktp2":
        if url:
            # bytes_
            bytes_ = _get_image_bytes_from_url(url)

        is_clear = _is_image_clear2(bytes_)
        if not is_clear["success"]:
            return is_clear

        res = _get_rekog_from_image_bytes(bytes_)
        return ktp.extract(res)

    if type_ == "ktp":
        if url:
            bytes_ = _get_image_bytes_from_url(url)
            print(bytes_[0:10])

        blocks = _get_textract_from_image_bytes(bytes_)["Blocks"]
        b = [
            block["Text"]
            for block in blocks
            if block["BlockType"] == "LINE" and block.get("Text")
        ]
        # print(b)
        from ocrs.textract import textract_lines_to_rekognition

        c = textract_lines_to_rekognition(b)
        return ktp.extract_from_list_of_str(c)

    if type_ == "npwp":
        if url:
            bytes_ = _get_image_bytes_from_url(url)
        res = _get_rekog_from_image_bytes(bytes_)
        return npwp.extract(res)

    # if type_ == "npwp-mini":
    #     urllib.request.urlretrieve(url, unique_filename)
    #     text_lines = via_subprocess.ocr_from_file(unique_filename).split("\n")
    #     return npwp_tesseract.extract_from_list_of_str(text_lines)

    # if type_ == "ktp-mini":
    #     urllib.request.urlretrieve(url, unique_filename)
    #     text_lines = via_subprocess.ocr_from_file(unique_filename).split("\n")
    #     return ktp_tesseract.extract_from_list_of_str(text_lines)


def lambda_handler(event, context):
    return main(event.get("url"), event["type"], event.get("base64"))


def test():
    pass