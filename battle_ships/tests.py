from .board import Board
from .game import BattleshipsGame


def test_ship_placement_valid():
    board = Board(5)
    coords = [(0, 0), (0, 1), (0, 2)]
    assert board.place_ship(coords) is True
    print("PASS: valid ship placement")


def test_ship_placement_overlap():
    board = Board(5)
    board.place_ship([(0, 0), (0, 1), (0, 2)])
    result = board.place_ship([(0, 2), (0, 3)])
    assert result is False
    print("PASS: overlapping ship placement rejected")


def test_shot_hit():
    board = Board(5)
    board.place_ship([(1, 1)])
    result = board.receive_shot(1, 1)
    assert result.status == "sunk"
    print("PASS: hit registered correctly")


def test_shot_miss():
    board = Board(5)
    board.place_ship([(1, 1)])
    result = board.receive_shot(0, 0)
    assert result.status == "miss"
    print("PASS: miss registered correctly")


def test_repeat_shot():
    board = Board(5)
    board.place_ship([(1, 1)])
    board.receive_shot(0, 0)
    result = board.receive_shot(0, 0)
    assert result.status == "repeat"
    print("PASS: repeat shot detected")


def test_win_condition():
    game = BattleshipsGame(5)
    game.player_board.place_ship([(0, 0)])
    game.computer_board.place_ship([(1, 1)])

    game.player_fire(1, 1)
    assert game.player_won() is True
    print("PASS: win condition detected")


def run_all_tests():
    print("=== Running Manual Tests ===")
    test_ship_placement_valid()
    test_ship_placement_overlap()
    test_shot_hit()
    test_shot_miss()
    test_repeat_shot()
    test_win_condition()
    print("=== All tests completed ===")


if __name__ == "__main__":
    run_all_tests()