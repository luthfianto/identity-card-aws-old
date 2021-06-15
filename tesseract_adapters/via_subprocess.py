import subprocess
TESSDATA_PREFIX='/opt/data/tessdata'
# TEMP_DIR = '/tmp/ocr'
# subprocess.check_output(f"mkdir -p {TEMP_DIR}", shell=True)

def ocr_from_file(filename):
    filename_ = filename.split(".")[-2]
    try:
        # command = f"tesseract {filename} {filename_} --psm 6"
        command = f"OMP_THREAD_LIMIT=1 TESSDATA_PREFIX={TESSDATA_PREFIX} tesseract {filename} {filename_} --psm 6"
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        res = open(f"{filename_}.txt").read()
        return res
    except Exception as e:
        print(e)
        raise e

