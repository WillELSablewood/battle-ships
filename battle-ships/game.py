import random
from board import Board
from ai import ComputerAI
from utils import parse_coordinate


class BattleshipsGame:
    def __init__(self, size: int):
        self.size = size
        self.player_board = Board(size)
        self.computer_board = Board(size)
        self.computer_ai = ComputerAI(size)

    def random_ship(self, length: int):
        while True:
            orientation = random.choice(["H", "V"])
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)

            ship = []
            for i in range(length):
                r = row + (i if orientation == "V" else 0)
                c = col + (i if orientation == "H" else 0)

                if r >= self.size or c >= self.size:
                    break

                ship.append((r, c))

            if len(ship) == length:
                return ship

    def setup_ships(self):
        for length in [3, 2]:
            self.player_board.place_ship(self.random_ship(length))
            self.computer_board.place_ship(self.random_ship(length))

    def player_turn(self):
        while True:
            guess = input("Enter a coordinate (e.g. A5): ").strip()
            coord = parse_coordinate(guess, self.size)

            if not coord:
                print("Invalid or off-grid coordinate. Try again.")
                continue

            row, col = coord
            result = self.computer_board.receive_shot(row, col)

            if result == "repeat":
                print("You already tried that coordinate.")
                continue

            print(f"You {result.upper()}!")
            return

    def computer_turn(self):
        row, col = self.computer_ai.take_shot()
        result = self.player_board.receive_shot(row, col)
        print(f"Computer fires at {chr(col + 65)}{row + 1}: {result.upper()}")

    def play(self):
        print("\nYour board:")
        self.player_board.display(reveal=True)

        print("\nEnemy board:")
        self.computer_board.display()

        self.player_turn()
        self.computer_turn()
