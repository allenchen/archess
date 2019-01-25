import random

class Chess(object):    
    def __init__(self, id):
        self.id = id

    def attack_rate(self):
        pass

    def damage(self):
        pass

    def attack_range(self):
        pass

    def bonuses(self, board_state):
        pass
    
    def select_target(self, targets):
        return random.sample(targets, 1)[0]

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
        return 1

    def attack_range(self):
        return 3

    def damage(self):
        damage_dealt = 3
        
        crit_roll = random.randint(1,10)

        if crit_roll > 9:
            damage_dealt = 100

        return damage_dealt

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

    def attack_range(self):
        return 1

    def damage(self):
        return random.randint(1,4)

    def bonuses(self, board_state):
        return []

    def starting_health(self):
        return 45

    def chess_type(self):
        return "Sven1"

class Zeus1Chess(Chess):
    def __init__(self, id, owner):
        self.id = id
        self.owner = owner

    def attack_rate(self):
        return 4

    def damage(self):
        return 50

    def attack_range(self):
        return 8

    def bonuses(self, board_state):
        return []

    def starting_health(self):
        return 20

    def chess_type(self):
        return "Zeus1"
