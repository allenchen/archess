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

board1 = BattleBoard(None)
board1.players = [player1, player2]

board1.chesses_owned = {
    player1: [],
    player2: []
}

add_piece(board1, c_zeus(player1), (2,0))
add_piece(board1, c_zeus(player1), (4,0))
add_piece(board1, c_storm(player1), (5,0))

add_piece(board1, c_sven(player2), (0,7))
add_piece(board1, c_sven(player2), (1,7))
add_piece(board1, c_sven(player2), (2,7))
add_piece(board1, c_sven(player2), (3,7))
add_piece(board1, c_sven(player2), (4,7))
add_piece(board1, c_storm(player2), (5,7))

print(board1.chesses_positions)

board1.battle()
