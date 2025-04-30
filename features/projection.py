import re
from unidecode import unidecode

def replace_caps_and_punct(obj):
    if isinstance(obj, dict):
        return {k: replace_caps_and_punct(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_caps_and_punct(elem) for elem in obj]
    elif isinstance(obj, str):
        return re.sub(r'[^\w\s]', '.', unidecode(obj).lower())
    else:
        return obj
    