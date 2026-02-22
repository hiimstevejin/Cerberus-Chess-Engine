import chess
from src.evals import evaluate_board


def negamax(board, depth):
    if depth == 0 or board.is_game_over():
      multiplier = 1 if board.turn == chess.WHITE else -1
      return multiplier * evaluate_board(board)

    best = float('-inf')

    for move in board.legal_moves:
        board.push(move)
        score = -1 * negamax(board, depth-1)
        board.pop()

        if (score > best):
            best = score
    return best
