import re

from . import mail

# import unidecode


def slugify(text):
    # text = unidecode.unidecode(text)
    return re.sub(r"[\W_]+", "_", text.lower())


def extract_uniques(elements, comp=lambda left, right: left == right):
    keep = []
    for e in elements:
        if not any(comp(e, k) for k in keep):
            keep.append(e)
    return keep
