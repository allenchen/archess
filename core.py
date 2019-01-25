import random

class Player(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return "Player{}".format(self.id)

class InventoryBoard(object):
    def __init__(self, player, chesses):
        self.player = player
        self.chesses = chesses
            
class DamageEffect(object):
    def __init__(self, source, target, amount):
        self.source = source
        self.target = target
        self.amount = amount

    def __str__(self):
        return "{} dealt {} damage to {}.".format(self.source, self.amount, self.target)

class BoardPositions(object):
    def __init__(self):
        self.position_lookup = [[None] * 8] * 8
        self.reverse_position_lookup = {}

    # position is a tuple (x,y)
    def add_piece(self, piece, position):
        x, y = position
        if self.position_lookup[x][y]:
            raise Exception("Can't add a piece at a location where there is already a piece.")
        self.position_lookup[x][y] = piece
        self.reverse_position_lookup = { piece: position }
        return self

    def remove_by_position(self, position):
        x, y = position
        piece = self.position_lookup[x][y]
        self.position_lookup[x][y] = None
        del self.reverse_position_lookup[piece]
        return self
    
    def remove_by_piece(self, piece):
        x, y = self.reverse_position_lookup[piece]
        del self.reverse_position_lookup[piece]
        self.position_lookup[x][y] = None
        return self

    def get_by_position(self, position):
        return self.position_lookup[x][y]

    def get_by_piece(self, piece):
        return self.reverse_position_lookup[piece]

    def get_available_targets(self, position, range):
        piece_x, piece_y = position
        # add one because it's an exclusive range, and I don't remember and I don't have internet
        # connection to find out what's the inclusive range syntax
        x_range = range(max(0, piece_x - range), min(8, piece_x + range + 1))
        y_range = range(max(0, piece_y - range), min(8, piece_y + range + 1))

        available_targets = []
        
        for x in x_range:
            for y in y_range:
                if self.position_lookup[x][y]:
                    available_targets += self.position_lookup[x][y]

        return available_targets

    def get_available_positions(self):
        available_positions = []
        for x in range(0,8):
            for y in range(0,8):
                if not self.position_lookup[x][y]:
                    available_positions += [(x, y)]
        return available_positions

    def move_piece(self, piece, new_position):
        old_x, old_y = self.reverse_position_lookup[piece]
        new_x, new_y = new_position
        if self.position_lookup[new_x][new_y]:
            raise Exception("Can't move a piece to a position where there is already a piece.")
        self.position_lookup[old_x][old_y] = None
        self.position_lookup[new_x][new_y] = piece
        self.reverse_position_lookup[piece] = new_position
        return self

class BattleBoard(object):
    def __init__(self, board_state):
        if board_state is None:
            self.players = []
            self.chesses_owned = {}
            self.chesses_health = {}
            self.chesses_positions = BoardPositions()

    def battle(self):
        timer = 1
        while not self.end_condition():
            effects_queue = []
            for player in self.players:
                for chess in self.chesses_owned[player]:
                    if timer % chess.attack_rate() == 0:
                        target = chess.select_target(self)
                        damage = self.calculate_damage(chess, target)
                        effects_queue += [DamageEffect(chess, target, damage)]
            
            effects_queue = self.apply_effect_priority(effects_queue)

            self.apply_effects(effects_queue)
            
            timer += 1
            print("-- Round {} Complete --".format(timer))

        print("Finished battle!")
        print(self)

    def determine_action(self, piece):
        
    
    def apply_effect_priority(self, effects):
        return random.sample(effects, len(effects))
    
    def apply_effects(self, effects):
        for effect in effects:
            # Remove health from target
            # Chesses only do damage if they are alive.
            if (self.piece_is_alive(effect.target) and self.piece_is_alive(effect.source)):

                target_health = self.chesses_health[effect.target]

                result_target_health = target_health - effect.amount

                print(effect)
                
                if result_target_health <= 0:
                    print("{} died!".format(effect.target))
                    self.chesses_owned[effect.target.owner].remove(effect.target)
                    del self.chesses_health[effect.target]
                else:
                    self.chesses_health[effect.target] = result_target_health
                    
            else:
                print("Tried to apply effect: {} - but could not find source or target.".format(effect))
                    
    def piece_is_alive(self, piece):
        return (
            piece in self.chesses_health and
            piece in self.chesses_owned[piece.owner] and
            self.chesses_health[piece] > 0)
    
    def calculate_damage(self, attacker, defender):
        return attacker.damage()
            
    def end_condition(self):
        return 0 in [len(chesses) for chesses in self.chesses_owned.values()]

    def opponent(self, player):
        return [p for p in self.players if p.id != player.id][0]

    def opponent_chesses(self, player):
        return self.chesses_owned[self.opponent(player)]
    
    def __str__(self):
        return str(
            [
                "{}: {}".format(
                    str(player),
                    ["{} ({} HP)".format(chess, self.chesses_health[chess]
                    ) for chess in chesses]
                )
                for player, chesses
                in self.chesses_owned.items()
        ])
