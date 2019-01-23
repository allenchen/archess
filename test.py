from core import *
import chess_types as CT

def generate_id():
    return 

player1 = Player(1, "Player 1")
player2 = Player(2, "Player 2")

p1_storm1_chess = CT.Storm1Chess(100, player1)
p1_storm1_chess2 = CT.Storm1Chess(101, player1)
p1_sven1_chess = CT.Sven1Chess(102, player1)

p2_storm1_chess = CT.Storm1Chess(200, player2)
p2_storm1_chess2 = CT.Storm1Chess(201, player2)
p2_sven1_chess = CT.Sven1Chess(202, player2)

board1 = BattleBoard(None)
board1.players = [player1, player2]
board1.chesses_owned = {
    player1: [p1_storm1_chess, p1_storm1_chess2, p1_sven1_chess],
    player2: [p2_storm1_chess, p2_storm1_chess2, p2_sven1_chess]
}
board1.chesses_health = {
    p1_storm1_chess: p1_storm1_chess.starting_health(),
    p1_storm1_chess2: p1_storm1_chess2.starting_health(),
    p1_sven1_chess: p1_sven1_chess.starting_health(),
    p2_storm1_chess: p2_storm1_chess.starting_health(),
    p2_storm1_chess2: p2_storm1_chess2.starting_health(),
    p2_sven1_chess: p2_sven1_chess.starting_health()
}

board1.battle()
