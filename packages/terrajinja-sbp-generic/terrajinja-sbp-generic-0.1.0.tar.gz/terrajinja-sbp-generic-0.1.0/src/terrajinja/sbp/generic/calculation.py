import re


class InvalidSizeUnit(Exception):
    """Unexpected size unit"""


def human_read_to_megabyte(size: str) -> int:
    """
    Convert human formatted size to megabytes value.

    Args:
        size: string of human formatted size

    Returns:
        megabytes represented in the initial human format

    """
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    size_split = re.split(r"(\d+)\s*([A-Z]+)", size.upper())

    if len(size_split) < 2:
        raise ValueError(f"expected format '$number$unit' got '{size}'")

    num, unit = int(size_split[1]), size_split[2].upper()
    if unit not in size_name:
        raise InvalidSizeUnit(f"the provided {size} does not have a valid unit '{unit}', expected one of {size_name}")
    idx = size_name.index(unit) - 2  # index in list of sizes determines power to raise it to
    factor = 1024 ** idx  # ** is the "exponent" operator - you can use it instead of math.pow()
    return num * factor
