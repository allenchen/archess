from core import *
import chess_types as CT

global CURRENT_ID
CURRENT_ID = 100

def generate_id():
    global CURRENT_ID
    CURRENT_ID += 1
    return CURRENT_ID

def c_storm(owner):
    return CT.Storm1Chess(generate_id(), owner)

def c_sven(owner):
    return CT.Sven1Chess(generate_id(), owner)

def c_zeus(owner):
    return CT.Zeus1Chess(generate_id(), owner)

def add_piece(board, piece, location):
    board.chesses_owned[piece.owner] += [piece]
    board.chesses_health[piece] = piece.starting_health()
    board.chesses_positions.add_piece(piece, location)

player1 = Player(1, "Player 1")
player2 = Player(2, "Player 2")

gs = GameState(1001)

gs.add_player(player1)
gs.add_player(player2)

gs.modify_gold(player1, 50)
gs.modify_gold(player2, 50)

z1 = gs.buy_chess(player1, c_zeus(player1))
gs.move_chess(player1, z1, (1, 0))
z2 = gs.buy_chess(player1, c_zeus(player1))
gs.move_chess(player1, z2, (4, 0))

s1 = gs.buy_chess(player2, c_sven(player2))
gs.move_chess(player2, s1, (1,0))
s2 = gs.buy_chess(player2, c_sven(player2))
gs.move_chess(player2, s2, (2,0))
s3 = gs.buy_chess(player2, c_sven(player2))
gs.move_chess(player2, s3, (3,2))
s4 = gs.buy_chess(player2, c_sven(player2))
gs.move_chess(player2, s4, (4,2))

gs.battle(player1, player2)
