def sanitize(string: str):
    string = string.replace(":", "").replace("!", "I")
    return " ".join(filter(lambda s: s.isupper(), string.split(" ")))


exclude_semicolon = sanitize

ERROR_COULD_NOT_EXTRACT_TEXT = "COULD_NOT_EXTRACT_TEXT"
