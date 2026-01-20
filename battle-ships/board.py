import string


class Board:
    def __init__(self, size: int):
        self.size = size
        self.grid = [["~" for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.shots_taken = set()

    def place_ship(self, ship: list):
        for r, c in ship:
            self.grid[r][c] = "S"
        self.ships.append(set(ship))

    def receive_shot(self, row: int, col: int):
        if (row, col) in self.shots_taken:
            return "repeat"

        self.shots_taken.add((row, col))

        for ship in self.ships:
            if (row, col) in ship:
                ship.remove((row, col))
                if not ship:
                    self.ships.remove(ship)
                    return "sunk"
                return "hit"

        return "miss"

    def all_ships_sunk(self):
        return len(self.ships) == 0

    def display(self, reveal=False):
        letters = string.ascii_uppercase[: self.size]
        header = "  " + " ".join(letters)
        print(header)

        for i, row in enumerate(self.grid):
            line = []
            for j, cell in enumerate(row):
                if cell == "S" and not reveal:
                    line.append("~")
                else:
                    line.append(cell)
            print(f"{i + 1:2} " + " ".join(line))
            