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
    """
    Perform Negamax search with alpha-beta pruning.

    This function searches the game tree recursively to give a given depth and returns the best eval score from perspective of side to move

    the implementation follows the Negamax formulation of Minimax:
        score(position) = -score(opponent_position)

    Alpha-beta pruning is used to eliminate branches that cannot affect the final decision, significantly reducing the number of nodes searched.

    Args:
        board (chess.Board):
            Current chess position.

        alpha (int):
            Lower bound of the search window (best already guaranteed score)

        beta (int):
            Upper bound of the search window (opponent's best alternative)

        depth (int):
            Remaining search depth

    Returns:
        int:
            Evaluation score from the perspective of the side to move
            Positive -> good for side to move
            Negative -> bad for side to move

    Search behavior:
        - When depth reaches 0, switches to quiescence search to avoid the horizon effect
        - Detects checkmate/stalemate if no legal moves exist
        - Uses simple move ordering (captures first) to improve pruning
    """
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
    """
    Perform quiescence search to stabilize tactical positions.

    Quiescence search extends evaluation beyond the normal depth limit by exploring only critical moves (currently captures). This prevents the engine from evaluating unstable positions where an immediate capture or recapture would drastically change the score

    The function first evaluates the current position ("stand pat" score), then recursively searches all capture moves using the Negamax framework

    Args:
        board (chess.Board):
            Current chess position.

        alpha (int):
            Lower bound of the search window

        beta (int):
            Upper bound of the search window

    Returns:
        int:
            Stabilized evaluation score after resolving capture sequences.

    Methods:
        1. Evaluate current position (stand-pat score)
        2. Apply alpha-beta cuttoff if possible
        3. Generate capture moves only
        4. Recursively search captures until position is quiet
    """
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
