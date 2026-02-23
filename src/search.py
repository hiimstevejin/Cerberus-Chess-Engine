import chess
from src.evals import evaluate_board

# for benchmarking purposes count node computation for search
nodes_count = 0

def get_nodes_count():
    global nodes_count
    count = nodes_count
    nodes_count = 0
    return count

def negamax(board:chess.Board, alpha:int, beta:int, depth:int):

    global nodes_count
    nodes_count += 1

    if depth == 0:
      return quiescence(board, alpha, beta)

    moves = list(board.legal_moves)

    if not moves:
        if board.is_check():
            return -100000 + depth
        else:
          return 0

    moves.sort(key=lambda m: board.is_capture(m), reverse=True)

    for move in moves:
        board.push(move)
        score = -negamax(board, -beta, -alpha, depth-1)
        board.pop()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

    return alpha

def quiescence(board, alpha, beta):

    global nodes_count
    nodes_count += 1

    base_score = evaluate_board(board)
    stand_pat = base_score if board.turn == chess.WHITE else -base_score

    if stand_pat >= beta:
        return beta
    if stand_pat > alpha:
        alpha = stand_pat

    moves = [m for m in board.legal_moves if board.is_capture(m)]

    for move in moves:
        board.push(move)
        score = -quiescence(board, -beta, -alpha)
        board.pop()

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha
