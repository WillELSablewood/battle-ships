import string


def parse_coordinate(coord: str, size: int):
    if len(coord) < 2:
        return None

    letter = coord[0].upper()
    number = coord[1:]

    if letter not in string.ascii_uppercase[:size]:
        return None

    if not number.isdigit():
        return None

    row = int(number) - 1
    col = string.ascii_uppercase.index(letter)

    if row < 0 or row >= size:
        return None

    return row, col