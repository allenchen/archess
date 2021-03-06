import random

class Player(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return "P{}".format(self.id)

    def __hash__(self):
        return self.id

class GameState(object):
    def __init__(self, id):
        self.players = []
        self.id = id
        self.chess_inventories = {}
        self.gold = {}
        self.chesses_positions = {}

    def add_player(self, player):
        if player in self.players:
            raise Exception("Player is already in this game!")
        
        self.players += [player]
        self.chess_inventories[player] = []
        self.gold[player] = 0
        self.chesses_positions[player] = BoardPositions()

    def modify_gold(self, player, delta):
        self.gold[player] += delta
        return self.gold[player]
        
    def buy_chess(self, player, chess):
        if self.gold[player] < chess.cost():
            raise Exception("Can't buy this chess because you don't have enough gold!")

        self.gold[player] -= chess.cost()

        self.add_to_inventory(player, chess)

        return chess
    
    def sell_chess(self, player, chess):
        pass

    def move_chess(self, player, chess, new_position):
        # y must be <= 3, you can only put units on the first four rows.

        if chess not in self.chess_inventories[player]:
            raise Exception("This chess isn't in your inventory!")

        new_x, new_y = new_position
        if new_y > 3:
            raise Exception("You can only put units on the first four rows")

        if self.chesses_positions[player].has_location(chess):
            self.chesses_positions[player].move_piece(chess, new_position)
        else:
            self.chesses_positions[player].add_piece(chess, new_position)

    def add_to_inventory(self, player, chess):
        self.chess_inventories[player] += [chess]

    def flip_pieces_and_add(self, source_board, delta_board):
        # adds delta_board to source_board (by creating a new board entirely) by flipping delta_board
        # over the x axis and adding it

        new_board = BoardPositions()
        for piece, position in delta_board.reverse_position_lookup.items():
            # flip location
            old_x, old_y = position
            new_position = (old_x, 7 - old_y)
            new_board.add_piece(piece, new_position)

        for piece, position in source_board.reverse_position_lookup.items():
            new_board.add_piece(piece, position)

        return new_board
        
    def battle(self, bottom_player, top_player):
        # initialize a battle given inventories and positions

        # create a single board
        battle_positions = self.flip_pieces_and_add(
            self.chesses_positions[bottom_player],
            self.chesses_positions[top_player]
        )

        # find all battle-ready combatants (with a position)
        bottom_player_chesses = [ chess
                                  for chess
                                  in self.chess_inventories[bottom_player]
                                  if self.chesses_positions[bottom_player].has_location(chess) ]

        top_player_chesses = [ chess
                               for chess
                               in self.chess_inventories[top_player]
                               if self.chesses_positions[top_player].has_location(chess) ]

        starting_chess_health = {
            chess: chess.starting_health() for chess in bottom_player_chesses + top_player_chesses
        }
        
        battle_board = BattleBoard(
            [bottom_player, top_player],
            { bottom_player: bottom_player_chesses,
              top_player: top_player_chesses },
            starting_chess_health,
            battle_positions
        )

        return battle_board.battle()        

class PurchaseChessEvent(object):
    def __init__(self, player, chess, spend):
        self.player = player
        self.chess = chess
        self.spend = spend

    def __str__(self):
        return "{} bought a {} for {} gold.".format(player, chess, spend)

class InitiateBattleEvent(object):
    def __init__(self, p1board, p2board):
        self.p1board = p1board
        self.p2board = p2board

    def __str__(self):
        return "A battle was initiated!"

class DamageEffect(object):
    def __init__(self, source, target, amount):
        self.source = source
        self.target = target
        self.amount = amount

    def __str__(self):
        return "{} dealt {} damage to {}.".format(self.source, self.amount, self.target)

class MoveEvent(object):
    def __init__(self, piece, old_position, new_position):
        self.piece = piece
        self.old_position = old_position
        self.new_position = new_position
        
    def __str__(self):
        return "{} moved from {} to {}".format(self.piece, self.old_position, self.new_position)

class DeathEvent(object):
    def __init__(self, piece):
        self.piece = piece

    def __str__(self):
        return "{} died!".format(self.piece)
    
class BattleEvent(object):
    def __init__(self):
        self.damage_effect = None
        self.move = None
        self.death = None
    
class BoardPositions(object):
    def __init__(self):
        self.position_lookup = [[None for x in range(8)] for x in range(8)]
        self.reverse_position_lookup = {}

    # position is a tuple (x,y)
    def add_piece(self, piece, position):
        x, y = position
        if self.position_lookup[x][y]:
            print(self.position_lookup)
            raise Exception("Can't add a piece at a location where there is already a piece.")
        self.position_lookup[x][y] = piece
        self.reverse_position_lookup[piece] = position
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

    def get_piece_at_location(self, position):
        return self.position_lookup[x][y]

    def get_piece_location(self, piece):
        return self.reverse_position_lookup[piece]

    def has_location(self, piece):
        return piece in self.reverse_position_lookup

    def get_available_targets(self, position, attack_range):
        piece_x, piece_y = position

        # add one because it's an exclusive range at the end
        x_range = range(max(0, piece_x - attack_range), min(8, piece_x + attack_range + 1))
        y_range = range(max(0, piece_y - attack_range), min(8, piece_y + attack_range + 1))
        
        available_targets = []
        
        for x in x_range:
            for y in y_range:
                if self.position_lookup[x][y]:
                    available_targets += [self.position_lookup[x][y]]

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

    def __str__(self):
        output = ""
        for y in range(0,8):
            output += " "
            for x in range(0,8):
                if self.position_lookup[x][y]:
                    output += "[{}]".format(self.position_lookup[x][y].short_name())
                else:
                    output += "[   ]"
            output += "\n"
        return output

class BattleBoard(object):
    def __init__(self, players, chesses_owned, chesses_health, chesses_positions):
        self.players = players
        self.chesses_owned = chesses_owned
        self.chesses_health = chesses_health
        self.chesses_positions = chesses_positions

    def battle(self):
        timer = 1
        while not self.end_condition():
            events = []
            
            chesses_to_act = []
            for player in self.players:
                for chess in self.chesses_owned[player]:
                    chesses_to_act += [chess]
            random.shuffle(chesses_to_act)
            
            for chess in chesses_to_act:
                if not self.piece_is_alive(chess):
                    continue
                
                targets = [ target for target in
                            self.chesses_positions.get_available_targets(self.chesses_positions.get_piece_location(chess), chess.attack_range())
                            if target.owner == self.opponent(chess.owner)
                ]

                if len(targets) == 0:
                    # move thie piece randomly
                    old_position = self.chesses_positions.get_piece_location(chess)
                    available_positions = self.chesses_positions.get_available_positions()
                    if len(available_positions) == 0:
                        raise Exception("No places for this piece to move!")
                        
                    new_position = random.choice(available_positions)
                        
                    self.chesses_positions.move_piece(chess, new_position)
                    events += [MoveEvent(chess, old_position, new_position)]
            
                else:
                    if timer % chess.attack_rate() == 0:
                        target = chess.select_target(targets)
                        damage = self.calculate_damage(chess, target)
                        effect = DamageEffect(chess, target, damage)
                        resulting_events = self.apply_effects([effect])
                        events += resulting_events
                        events += [effect]

            for event in events:
                print (event)
                
            print(self.chesses_positions)
            print(self.print_unit_summary())

            print("-- Round {} Complete --".format(timer))
            
            timer += 1

        print("Finished battle!")
        print(self)
    
    def apply_effects(self, effects):
        events = []
        
        for effect in effects:
            # Remove health from target
            # Chesses only do damage if they are alive.
            if (self.piece_is_alive(effect.target) and self.piece_is_alive(effect.source)):
                target_health = self.chesses_health[effect.target]
                result_target_health = target_health - effect.amount
                
                if result_target_health <= 0:
                    events += [DeathEvent(effect.target)]
                    self.chesses_owned[effect.target.owner].remove(effect.target)
                    del self.chesses_health[effect.target]
                    self.chesses_positions.remove_by_piece(effect.target)
                else:
                    self.chesses_health[effect.target] = result_target_health
                    
            else:
                print("Tried to apply effect: {} - but could not find source or target.".format(effect))

        return events
                    
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

    def print_unit_summary(self):
        output = ""
        for player in self.players:
            output += "{} units:\n".format(player)
            for chess in self.chesses_owned[player]:
                output += "    {}\n".format(self.display_chess_health(chess))
        return output

    def display_chess_health(self, piece):
        current_health = self.chesses_health[piece]
        max_health = piece.starting_health()
        missing_health = max_health - current_health

        health_display = "[{}{}]".format("■" * current_health, " " * missing_health)

        padding = 25 - len(str(piece))
        if padding < 0:
            padding = 0
        unit_name_display = "{}{}".format(piece, " " * padding)
        
        return "{}: {}".format(unit_name_display, health_display)
    
    def __str__(self):
        return str(self.chesses_positions) + str(
            [
                "{}: {}".format(
                    str(player),
                    ["{} ({} HP)".format(chess, self.chesses_health[chess]
                    ) for chess in chesses]
                )
                for player, chesses
                in self.chesses_owned.items()
        ])
