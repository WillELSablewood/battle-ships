from .game import BattleshipsGame
from .utils import coord_to_label, parse_coordinate


TITLE = "battle-ships"


def get_grid_size() -> int:
    while True:
        raw = input("Choose grid size (5–10): ").strip()

        if raw == "":
            print("Please enter a number.")
            continue

        if not raw.isdigit():
            print("Invalid input. Enter a number from 5 to 10.")
            continue

        size = int(raw)
        if size < 5 or size > 10:
            print("Grid size must be between 5 and 10.")
            continue

        return size


def print_status(size: int, shots_taken: int) -> None:
    letters = "".join(chr(ord("A") + i) for i in range(size))
    print()
    print(f"Columns: {letters}")
    print(f"Rows:    1..{size}")
    print(f"Shots taken: {shots_taken}")
    print()


def main() -> None:
    print(f"=== {TITLE} ===")
    print("Sink all enemy ships. Enter shots like A5.")
    print()

    size = get_grid_size()
    game = BattleshipsGame(size)
    game.setup_ships()

    while True:
        print_status(size, shots_taken=len(game.computer_board.shots_taken))

        # Player turn (validate until a non-repeat valid shot happens)
        while True:
            guess = input("Fire at: ").strip()
            coord = parse_coordinate(guess, size)

            if coord is None:
                print("Invalid or off-grid coordinate. Try again (e.g., A1).")
                continue

            row, col = coord
            result = game.player_fire(row, col)

            if result.status == "repeat":
                print(result.message)
                continue

            print(result.message)
            break

        if game.player_won():
            print()
            print("You WIN! All enemy ships are sunk.")
            return

        # Computer turn
        c_row, c_col, c_result = game.computer_fire()
        print(f"Computer fires at {coord_to_label(c_row, c_col)}: {c_result.message}")

        if game.computer_won():
            print()
            print("You LOSE. Your fleet has been destroyed.")
            return


if __name__ == "__main__":
    main()