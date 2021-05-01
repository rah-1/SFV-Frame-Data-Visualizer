from move import Move


class Character:
    def __init__(self, name, hp, stun):
        self.name = name
        self.hp = hp
        self.stun = stun
        self.moveset = []

    def add_move(self, move):
        self.moveset.append(move)

