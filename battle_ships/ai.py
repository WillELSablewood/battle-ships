import random


class ComputerAI:
    """
    Simple AI: random shots without repeats.
    """

    def __init__(self, size: int) -> None:
        self.size = size
        self._shots = [(r, c) for r in range(size) for c in range(size)]
        random.shuffle(self._shots)

    def take_shot(self) -> tuple[int, int]:
        return self._shots.pop()