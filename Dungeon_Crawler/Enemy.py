from random import randint


class Enemy:

    def __init__(self, health, position=None, player_turn=True):
        self.health = health
        self.position = position
        self.player_turn = player_turn

    def spawn(self) -> list:
        x = randint(1, 4)
        y = randint(0, 4)
        if x == 4 and y == 4:
            x = 3
            y = 4
            self.position = [x, y]
        else:
            self.position = [x, y]
        return self.position

    def get_position(self) -> list:
        return self.position

    def movement(self, player_pos=list) -> list:
        self.get_position()
        direction = randint(0, 1)
        if direction == 0:
            try:
                if player_pos[0] >= self.position[0]:
                    self.position[0] += 1
                elif player_pos[0] <= self.position[0]:
                    self.position[0] -= 1
            except self.position[0] > 4 or self.position[0] < 0:
                pass
        elif direction == 1:
            try:
                if player_pos[1] >= self.position[1]:
                    self.position[1] += 1
                elif player_pos[1] <= self.position[1]:
                    self.position[1] -= 1
            except self.position[1] > 4 or self.position[1] < 0:
                pass
        return self.position

