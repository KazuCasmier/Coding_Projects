from random import randint


class Player:

    def __init__(self, health, position=None, in_combat=False, player_turn=True):
        if position is None:
            position = [0, 0]
        self.health = health
        self.position = position
        self.in_combat = in_combat
        self.player_turn = player_turn

    def get_pos(self) -> list:
        return self.position

    def movement(self, direction) -> list:

        if direction == 'up':
            self.position[1] -= 1
            return self.position

        elif direction == 'down':
            self.position[1] += 1
            return self.position

        elif direction == 'left':
            self.position[0] -= 1
            return self.position

        elif direction == 'right':
            self.position[0] += 1
            return self.position

    def start_combat(self):
        if self.in_combat:
            return self.player_turn
        else:
            self.in_combat = True
            turn_order = randint(1, 2)

            if turn_order == 1:
                self.player_turn = False
            elif turn_order == 2:
                self.player_turn = True

            return self.player_turn

    def run(self):
        if not self.in_combat:
            return 0, '\nYou are not in combat, you cannot run.'

        if self.in_combat is True:
            run_chance = randint(1, 3)

            if run_chance == 1:
                self.in_combat = False
                return 1, '\nYou are out of combat!!'

            else:
                self.in_combat = True
                return 2, '\nYou fail to run and are still in combat!!'
