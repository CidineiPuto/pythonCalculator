import re

NUM_OR_DOT_REGEX = re.compile(r"^[0-9.]$")


def isNumOrDot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))


def isValidNumber(string: str):
    valid = False
    try:
        float(string)
        valid = True
    except ValueError:
        valid = False
    return valid


def ConvertToNumber(string: str):
    number = float(string)

    if number.is_integer():  # Se puder ser um int, continuará sendo int
        number = int(number)

    return number


def isEmpty(string: str):
    return len(string) == 0
