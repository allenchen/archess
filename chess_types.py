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

    def short_name(self):
        return "???"

    def cost(self):
        return 100
    
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
        damage_dealt = 1
        
        crit_roll = random.randint(1,100)

        if crit_roll > 99:
            damage_dealt = 100

        return damage_dealt

    def bonuses(self, board_state):
        return []

    def starting_health(self):
        return 25

    def chess_type(self):
        return "Storm1"

    def short_name(self):
        return "ST{}".format(self.owner.id)

    def cost(self):
        return 5

class Sven1Chess(Chess):
    def __init__(self, id, owner):
        self.id = id
        self.owner = owner

    def attack_rate(self):
        return 3

    def attack_range(self):
        return 1

    def damage(self):
        return random.randint(2,9)

    def bonuses(self, board_state):
        return []

    def starting_health(self):
        return 45

    def chess_type(self):
        return "Sven1"

    def short_name(self):
        return "SV{}".format(self.owner.id)

    def cost(self):
        return 3

class Zeus1Chess(Chess):
    def __init__(self, id, owner):
        self.id = id
        self.owner = owner

    def attack_rate(self):
        return 6

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

    def short_name(self):
        return "ZE{}".format(self.owner.id)

    def cost(self):
        return 10
