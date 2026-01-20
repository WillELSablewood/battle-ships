from rich.console import Console
from rich.table import Table

from .game import BattleshipsGame
from .utils import coord_to_label, parse_coordinate

TITLE = "battle-ships"
console = Console()


def print_tracking_board(size: int, shot_map: list[list[str]]) -> None:
    table = Table(title="Enemy Waters (your shots)", show_lines=False)

    table.add_column("")
    for i in range(size):
        table.add_column(chr(ord("A") + i), justify="center")

    for r in range(size):
        row = [str(r + 1)]
        row.extend(shot_map[r])
        table.add_row(*row)

    console.print(table)
    console.print()


def print_grid(title: str, size: int, grid: list[list[str]]) -> None:
    table = Table(title=title, show_lines=False)

    table.add_column("")
    for i in range(size):
        table.add_column(chr(ord("A") + i), justify="center")

    for r in range(size):
        row = [str(r + 1)]
        row.extend(grid[r])
        table.add_row(*row)

    console.print(table)
    console.print()


def get_grid_size() -> int:
    while True:
        raw = input("Choose grid size (5–10): ").strip()

        if raw == "":
            console.print("[red]Please enter a number.[/red]")
            continue

        if not raw.isdigit():
            console.print(
                "[red]Invalid input.[/red] "
                "Enter a number from 5 to 10."
            )
            continue

        size = int(raw)
        if size < 5 or size > 10:
            console.print("[red]Grid size must be between 5 and 10.[/red]")
            continue

        return size


def print_status(size: int, shots_taken: int) -> None:
    letters = "".join(chr(ord("A") + i) for i in range(size))
    console.print()
    console.print(f"[bold]Columns:[/bold] {letters}")
    console.print(f"[bold]Rows:[/bold]    1..{size}")
    console.print(f"[bold]Shots taken:[/bold] {shots_taken}")
    console.print()


def format_player_result(status: str, message: str) -> str:
    if status == "hit":
        return "[bold green]Hit![/bold green]"
    if status == "miss":
        return "[blue]Miss![/blue]"
    if status == "sunk":
        return "[bold magenta]Sunk![/bold magenta]"
    if status == "repeat":
        return f"[yellow]{message}[/yellow]"
    return message


def main() -> None:
    console.print(f"[bold cyan]=== {TITLE} ===[/bold cyan]")
    console.print("Sink all enemy ships. Enter shots like A5.")
    console.print()

    size = get_grid_size()
    game = BattleshipsGame(size)
    game.setup_ships()

    while True:
        print_status(size, shots_taken=len(game.computer_board.shots_taken))
        print_grid("Your Fleet", size, game.player_board.fleet_view())
        print_tracking_board(size, game.computer_board.shot_map)

        # Player turn
        while True:
            guess = input("Fire at: ").strip()
            coord = parse_coordinate(guess, size)

            if coord is None:
                console.print(
                    "[red]Invalid or off-grid coordinate.[/red] "
                    "Try again (e.g., A1)."
                )
                continue

            row, col = coord
            result = game.player_fire(row, col)

            if result.status == "repeat":
                console.print(format_player_result
                              (result.status, result.message))
                continue

            console.print(format_player_result(result.status, result.message))
            break

        if game.player_won():
            console.print()
            console.print(
                "[bold green]You WIN! All enemy ships are sunk.[/bold green]"
            )
            return

        # Computer turn
        c_row, c_col, c_result = game.computer_fire()
        coord_label = coord_to_label(c_row, c_col)
        console.print(
            f"[yellow]Computer fires at {coord_label}:[/yellow] "
            f"{c_result.message}"
        )

        if game.computer_won():
            console.print()
            console.print(
                "[bold red]You LOSE. Your fleet has been destroyed.[/bold red]"
            )
            return


if __name__ == "__main__":
    main()