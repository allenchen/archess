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

class BattleBoard(object):
    def __init__(self, board_state):
        if board_state is None:
            self.players = []
            self.chesses_owned = {}
            self.chesses_health = {}

    def battle(self):
        timer = 1
        while not self.end_condition():
            effects_queue = []
            for player in self.players:
                for chess in self.chesses_owned[player]:
                    if timer % chess.attack_rate() == 0:
                        target = chess.select_target(self)
                        damage = chess.damage()
                        effects_queue += [DamageEffect(chess, target, damage)]
            
            effects_queue = self.apply_effect_priority(effects_queue)

            self.apply_effects(effects_queue)
            
            timer += 1

        print("Finished battle!")
        print(self)

    def apply_effect_priority(self, effects):
        return random.sample(effects, len(effects))
    
    def apply_effects(self, effects):
        for effect in effects:
            # Remove health from target
            if effect.target in self.chesses_health and effect.target in self.chesses_owned[effect.target.owner]:
                target_health = self.chesses_health[effect.target]

                result_target_health = target_health - effect.amount

                if result_target_health <= 0:
                    self.chesses_owned[effect.target.owner].remove(effect.target)
                    del self.chesses_health[effect.target]
                else:
                    self.chesses_health[effect.target] = result_target_health

                print(effect)
            else:
                print("Tried to apply effect: {} - but could not find target.".format(effect))
                    

    def calculate_damage(self, attacker, defender):
        return attacker.damage()
            
    def end_condition(self):
        return 0 in [len(chesses) for chesses in self.chesses_owned.values()]

    def opponent(self, player):
        return [p for p in self.players if p.id != player.id][0]

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
