import chess
from src.evals import evaluate_board
from src.search import Search
import time

DEPTH = 4
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
search = Search()
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
score,_ = search.negamax(board, -100000, 100000, DEPTH, 0)
test("Mate in 1 detected", score > MATE_SCORE - 2000)


#
# Stalemate test
#
board = chess.Board("7k/5K2/6Q1/8/8/8/8/8 b - - 1 1")
score,_ = search.negamax(board, -100000, 100000, DEPTH, 0)
test("Stalemate near 0", abs(score) < 50)


#
# Iterative Deepening test 20 sec
#
board = chess.Board()
best_move = search.start_search(board, time_limit=20)
test("Iterative Deepening", best_move is not None)

#
# Depth 5 test
#
board = chess.Board()

t0 = time.time()
score, _ = search.negamax(board, -100000, 100000, DEPTH, 0)
t1 = time.time()

print(f"Depth {DEPTH} time:", round(t1 - t0, 3), "seconds")
print("number of nodes:", search.nodes)
