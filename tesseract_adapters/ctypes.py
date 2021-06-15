import sys
import cv2
import ctypes
import ctypes.util

if sys.platform == "win32":
    LIBNAME = "libtesseract302"
else:
    LIBNAME = "tesseract"


class TesseractError(Exception):
    pass


class Tesseract(object):
    _lib = None
    _api = None

    class TessBaseAPI(ctypes._Pointer):
        _type_ = type("_TessBaseAPI", (ctypes.Structure,), {})

    @classmethod
    def setup_lib(cls, lib_path=None):
        if cls._lib is not None:
            return
        if lib_path is None:
            lib_path = ctypes.util.find_library(LIBNAME)
            if lib_path is None:
                raise TesseractError("tesseract library not found")
        cls._lib = lib = ctypes.CDLL(lib_path)

        # source:
        # https://github.com/tesseract-ocr/tesseract/
        #         blob/3.02.02/api/capi.h

        lib.TessBaseAPICreate.restype = cls.TessBaseAPI

        lib.TessBaseAPIDelete.restype = None  # void
        lib.TessBaseAPIDelete.argtypes = (cls.TessBaseAPI,)  # handle

        lib.TessBaseAPIInit3.argtypes = (
            cls.TessBaseAPI,  # handle
            ctypes.c_char_p,  # datapath
            ctypes.c_char_p,
        )  # language

        lib.TessBaseAPISetImage.restype = None
        lib.TessBaseAPISetImage.argtypes = (
            cls.TessBaseAPI,  # handle
            ctypes.c_void_p,  # imagedata
            ctypes.c_int,  # width
            ctypes.c_int,  # height
            ctypes.c_int,  # bytes_per_pixel
            ctypes.c_int,  # bytes_per_line
        )

        lib.TessBaseAPIGetUTF8Text.restype = ctypes.c_char_p
        lib.TessBaseAPIGetUTF8Text.argtypes = (cls.TessBaseAPI,)  # handle

        # psm
        lib.TessBaseAPISetPageSegMode.restype = None  # void
        lib.TessBaseAPISetPageSegMode.argtypes = (
            cls.TessBaseAPI,  # handle
            ctypes.c_int,  # mode
        )

    def __init__(self, language="eng", datapath=None, lib_path=None, psm=None):
        if self._lib is None:
            self.setup_lib(lib_path)
        self._api = self._lib.TessBaseAPICreate()

        if datapath:
            datapath = datapath.encode("utf-8")
        if language:
            language = language.encode("utf-8")
        if lib_path:
            lib_path = lib_path.encode("utf-8")

        if self._lib.TessBaseAPIInit3(self._api, datapath, language):
            print(self._api, datapath, language)
            raise TesseractError("initialization failed")

        if psm:
            self._lib.TessBaseAPISetPageSegMode(self._api, psm)

    def __del__(self):
        if not self._lib or not self._api:
            return
        if not getattr(self, "closed", False):
            self._lib.TessBaseAPIDelete(self._api)
            self.closed = True

    def _check_setup(self):
        if not self._lib:
            raise TesseractError("lib not configured")
        if not self._api:
            raise TesseractError("api not created")

    def set_image(self, imagedata, width, height, bytes_per_pixel, bytes_per_line=None):
        self._check_setup()
        if bytes_per_line is None:
            bytes_per_line = width * bytes_per_pixel
        self._lib.TessBaseAPISetImage(
            self._api, imagedata, width, height, bytes_per_pixel, bytes_per_line
        )

    def get_utf8_text(self):
        self._check_setup()
        return self._lib.TessBaseAPIGetUTF8Text(self._api)

    def get_text(self):
        result = self.get_utf8_text()
        if result:
            return result.decode("utf-8")


def ocr_from_file(filename):
    imcv = cv2.imread(filename)
    height, width, depth = imcv.shape

    tess = Tesseract(
        # language="ind",
        # datapath="./tessdata",
        lib_path=None,
        psm=6,
    )
    tess.set_image(imcv.ctypes, width, height, depth)
    text = tess.get_text()

    return text


if __name__ == "__main__":
    import time
    filename="zulkarnaen.jpeg"

    start_time = time.time()
    text = ocr_from_file(filename)
    print(time.time() - start_time)
    print(text)

    # text= text.strip()
    # print(text)
