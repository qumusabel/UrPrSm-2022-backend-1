import random
import re
from string import ascii_letters, digits

_slug_alph = ascii_letters + digits

_url_re = re.compile(
    r'^https?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def is_valid_url(url: str):
    return url is not None and _url_re.search(url)


def generate_slug(len: int = 11) -> str:
    return ''.join(random.choices(_slug_alph, k=len))    

