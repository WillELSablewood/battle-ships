import string


def parse_coordinate(text: str, size: int) -> tuple[int, int] | None:
    """
    Convert user input like 'A5' to (row, col) zero-based indexes.
    Returns None if invalid or off-grid.
    """
    cleaned = text.strip().upper().replace(" ", "")

    if len(cleaned) < 2:
        return None

    letter = cleaned[0]
    number = cleaned[1:]

    valid_letters = string.ascii_uppercase[:size]
    if letter not in valid_letters:
        return None

    if not number.isdigit():
        return None

    row = int(number) - 1
    col = valid_letters.index(letter)

    if row < 0 or row >= size:
        return None

    return row, col


def coord_to_label(row: int, col: int) -> str:
    """
    Convert (row, col) to a label like 'A5'.
    """
    return f"{chr(ord('A') + col)}{row + 1}"