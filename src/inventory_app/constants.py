import re

class BookRegex:

    YEAR_REGEX = re.compile(r"^([1-2]{1})?([0-9]{3})$gm")