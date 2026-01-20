from dataclasses import dataclass


@dataclass(frozen=True)
class ShotOutcome:
    status: str  # "hit", "miss", "sunk", "repeat"
    message: str


class Board:
    """
    Stores ship positions and tracks shots.

    Data:
    - ships: remaining coordinates per ship (hit squares removed)
    - ship_cells: all original ship coordinates (for fleet display)
    - shots_taken: all coordinates fired at
    - shot_map: shooter view (~ unknown, O miss, X hit)
    """

    def __init__(self, size: int) -> None:
        self.size = size
        self.ships: list[set[tuple[int, int]]] = []
        self.ship_cells: set[tuple[int, int]] = set()
        self.shots_taken: set[tuple[int, int]] = set()
        self.shot_map: list[list[str]] = [
            ["~" for _ in range(size)] for _ in range(size)
        ]

    def can_place_ship(self, coords: list[tuple[int, int]]) -> bool:
        """
        Return True if ship coordinates are in-bounds and non-overlapping.
        """
        if not coords:
            return False

        for row, col in coords:
            if row < 0 or row >= self.size:
                return False
            if col < 0 or col >= self.size:
                return False
            if (row, col) in self.ship_cells:
                return False

        return True

    def place_ship(self, coords: list[tuple[int, int]]) -> bool:
        """
        Place a ship if valid. Returns True if placed, False otherwise.
        """
        if not self.can_place_ship(coords):
            return False

        self.ships.append(set(coords))
        self.ship_cells.update(coords)
        return True

    def receive_shot(self, row: int, col: int) -> ShotOutcome:
        """
        Apply a shot to this board and return the result.
        """
        shot = (row, col)

        if shot in self.shots_taken:
            msg = "You already fired at that coordinate."
            return ShotOutcome("repeat", msg)

        self.shots_taken.add(shot)

        for ship in list(self.ships):
            if shot in ship:
                ship.remove(shot)
                self.shot_map[row][col] = "X"

                if not ship:
                    self.ships.remove(ship)
                    return ShotOutcome("sunk", "Sunk!")

                return ShotOutcome("hit", "Hit!")

        self.shot_map[row][col] = "O"
        return ShotOutcome("miss", "Miss!")

    def all_ships_sunk(self) -> bool:
        return len(self.ships) == 0

    def fleet_view(self) -> list[list[str]]:
        """
        Owner view of this board:
        ~ water, S ship, O miss, X hit
        """
        grid = [["~" for _ in range(self.size)] for _ in range(self.size)]

        for row, col in self.ship_cells:
            grid[row][col] = "S"

        for row, col in self.shots_taken:
            if (row, col) in self.ship_cells:
                grid[row][col] = "X"
            else:
                grid[row][col] = "O"

        return grid
    