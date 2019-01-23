import random

class Chess(object):    
    def __init__(self, id):
        self.id = id

    def attack_rate(self):
        pass

    def damage(self):
        pass

    def bonuses(self, board_state):
        pass
    
    def select_target(self, board_state):
        opponent_chesses = board_state.opponent_chesses(self.owner)
        if len(opponent_chesses) == 0:
            return None
        else:
            return random.sample(opponent_chesses, 1)[0]

    def starting_health(self):
        pass

    def __hash__(self):
        return self.id

    def __str__(self):
        return "[{} | {}]".format(self.chess_type(), self.owner)

class Storm1Chess(Chess):
    def __init__(self, id, owner):
        self.id = id
        self.owner = owner
        
    def attack_rate(self):
        return 2

    def damage(self):
        return 10

    def bonuses(self, board_state):
        return []

    def starting_health(self):
        return 25

    def chess_type(self):
        return "Storm1"

class Sven1Chess(Chess):
    def __init__(self, id, owner):
        self.id = id
        self.owner = owner

    def attack_rate(self):
        return 1

    def damage(self):
        return 2

    def bonuses(self, board_state):
        return []

    def starting_health(self):
        return 15

    def chess_type(self):
        return "Sven1"
