import random


class ComputerAI:
    def __init__(self, size: int):
        self.size = size
        self.available_shots = [
            (r, c) for r in range(size) for c in range(size)
        ]
        random.shuffle(self.available_shots)

    def take_shot(self):
        return self.available_shots.pop()

