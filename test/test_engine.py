import chess
from src.evals import evaluate_board
from src.search import negamax, get_nodes_count
import time

DEPTH = 5
MATE_SCORE = 90000


def test(name, condition):
    if condition:
        print(f"[PASS] {name}")
    else:
        print(f"[FAIL] {name}")

#
# STARTING POSITION TEST
#
board = chess.Board()
score = evaluate_board(board)
test("Start position eval == 0", score == 0)


#
# Mirror Symmetry test
#
board = chess.Board()
score1 = evaluate_board(board)
board = chess.Board().mirror()
score2 = evaluate_board(board)
test("Mirror symmetry", score1 == -score2)

#
# Material test
#
board = chess.Board()
board.remove_piece_at(chess.D8)
score = evaluate_board(board)
test("Black queen removed -> big white advantage", score > 800)

#
# Mate in 1 test
#
board = chess.Board("7k/5K2/6Q1/8/8/8/8/8 w - - 0 1")
score = negamax(board, -100000, 100000, DEPTH)
test("Mate in 1 detected", score > MATE_SCORE - 2000)


#
# Stalemate test
#
board = chess.Board("7k/5K2/6Q1/8/8/8/8/8 b - - 1 1")
score = negamax(board, -100000, 100000, 2)
test("Stalemate near 0", abs(score) < 50)


#
# Depth 5 test
#
board = chess.Board()

t0 = time.time()
negamax(board, -100000, 100000, 5)
t1 = time.time()
nodes = get_nodes_count()

print("Depth 5 time:", round(t1 - t0, 3), "seconds")
print("number of nodes:", nodes)
