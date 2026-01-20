from game import BattleshipsGame


def get_grid_size():
    while True:
        size_input = input("Choose grid size (5–10): ").strip()

        if not size_input.isdigit():
            print("Please enter a number.")
            continue

        size = int(size_input)

        if size < 5 or size > 10:
            print("Grid size must be between 5 and 10.")
            continue

        return size


def main():
    print("=== Battleships ===")
    size = get_grid_size()

    game = BattleshipsGame(size)
    game.setup_ships()

    while True:
        game.play()

        if game.computer_board.all_ships_sunk():
            print("\nYou WIN!")
            break

        if game.player_board.all_ships_sunk():
            print("\nYou LOSE!")
            break


if __name__ == "__main__":
    main()
