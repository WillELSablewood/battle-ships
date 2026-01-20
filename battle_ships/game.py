import random

from .ai import ComputerAI
from .board import Board, ShotOutcome


class BattleshipsGame:
    """
    Game coordinator: setup, turns, and win/lose state.
    """

    def __init__(self, size: int) -> None:
        self.size = size
        self.player_board = Board(size)
        self.computer_board = Board(size)
        self.computer_ai = ComputerAI(size)

    def setup_ships(self) -> None:
        """
        Places ships for both player and computer.
        Ship set: [3, 2, 2] keeps games short and readable for marking.
        """
        ship_lengths = [3, 2, 2]

        for length in ship_lengths:
            self._place_randomly(self.player_board, length)
            self._place_randomly(self.computer_board, length)

    def _place_randomly(self, board: Board, length: int) -> None:
        while True:
            coords = self._random_ship_coords(length)
            if board.place_ship(coords):
                return

    def _random_ship_coords(self, length: int) -> list[tuple[int, int]]:
        orientation = random.choice(["H", "V"])

        if orientation == "H":
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - length)
            return [(row, col + i) for i in range(length)]

        row = random.randint(0, self.size - length)
        col = random.randint(0, self.size - 1)
        return [(row + i, col) for i in range(length)]

    def player_fire(self, row: int, col: int) -> ShotOutcome:
        return self.computer_board.receive_shot(row, col)

    def computer_fire(self) -> tuple[int, int, ShotOutcome]:
        row, col = self.computer_ai.take_shot()
        outcome = self.player_board.receive_shot(row, col)
        return row, col, outcome

    def player_won(self) -> bool:
        return self.computer_board.all_ships_sunk()

    def computer_won(self) -> bool:
        return self.player_board.all_ships_sunk()