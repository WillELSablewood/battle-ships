from dataclasses import dataclass


@dataclass(frozen=True)
class ShotOutcome:
    status: str  # "hit", "miss", "sunk", "repeat"
    message: str


class Board:
    """
    Stores ship positions and tracks shots taken.

    ships: list of sets; each set contains remaining coordinates for a ship.
    shots_taken: set of all coordinates already fired at.
    """

    def __init__(self, size: int) -> None:
        self.size = size
        self.ships: list[set[tuple[int, int]]] = []
        self.shots_taken: set[tuple[int, int]] = set()

    def _occupied(self) -> set[tuple[int, int]]:
        if not self.ships:
            return set()
        return set().union(*self.ships)

    def can_place_ship(self, coords: list[tuple[int, int]]) -> bool:
        if not coords:
            return False

        occupied = self._occupied()

        for r, c in coords:
            if r < 0 or r >= self.size or c < 0 or c >= self.size:
                return False
            if (r, c) in occupied:
                return False

        return True

    def place_ship(self, coords: list[tuple[int, int]]) -> bool:
        """
        Place a ship if valid. Returns True if placed, False otherwise.
        """
        if not self.can_place_ship(coords):
            return False

        self.ships.append(set(coords))
        return True

    def receive_shot(self, row: int, col: int) -> ShotOutcome:
        """
        Apply a shot to this board.
        """
        shot = (row, col)

        if shot in self.shots_taken:
            return ShotOutcome("repeat", "You already fired at that coordinate.")

        self.shots_taken.add(shot)

        for ship in list(self.ships):
            if shot in ship:
                ship.remove(shot)
                if not ship:
                    self.ships.remove(ship)
                    return ShotOutcome("sunk", "Sunk!")
                return ShotOutcome("hit", "Hit!")

        return ShotOutcome("miss", "Miss!")

    def all_ships_sunk(self) -> bool:
        return len(self.ships) == 0