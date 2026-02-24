import chess
from src.evals import evaluate_board

# for benchmarking purposes count node computation for search
class Search:
    def __init__(self):
        # transposition table

        self.nodes = 0
        self.stop = False
        self.start_time = 0
        self.time_limit = 0

    def negamax(self, board:chess.Board, alpha:int, beta:int, depth:int, ply:int):
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
            chess.Move:
                Best move found

        Search behavior:
            - When depth reaches 0, switches to quiescence search to avoid the horizon effect
            - Detects checkmate/stalemate if no legal moves exist
            - Uses simple move ordering (captures first) to improve pruning
        """
        self.nodes += 1
        if board.is_game_over():
            if board.is_checkmate():
                return -100000 + ply, None
            else:
                return 0, None

        if depth == 0:
            return self.quiescence(board, alpha, beta), None

        moves = list(board.legal_moves)
        captures = [m for m in moves if board.is_capture(m)]
        quiet = [m for m in moves if not board.is_capture(m)]
        ordered_moves = captures + quiet
        best_move = None

        for move in ordered_moves:
            board.push(move)
            child_score, _ = self.negamax(board, -beta, -alpha, depth-1, ply + 1)
            score = -child_score
            board.pop()

            if score >= beta:
                return beta, move
            if score > alpha:
                alpha = score
                best_move = move

        if best_move is None and ordered_moves:
              best_move = ordered_moves[0]

        return alpha, best_move

    def quiescence(self, board, alpha, beta):
        """
        Perform quiescence search to stabilize tactical positions.

        Quiescence search extends evaluation beyond the normal depth limit by exploring only critical moves (currently captures). This prevents the engine from evaluating unstable positions where an immediate capture or recapture would drastically change the score

        The function first evaluates the current position ("stand pat" score), then recursively searches all capture moves using the Negamax framework

        The implementation follows the Quiescence search found in ChessProgramming Wiki
        https://www.chessprogramming.org/Quiescence_Search

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
        self.nodes += 1

        base_score = evaluate_board(board)
        stand_pat = base_score if board.turn == chess.WHITE else -base_score
        best_value = stand_pat

        if stand_pat >= beta:
            return stand_pat

        if stand_pat > alpha:
            alpha = stand_pat

        enemy_color = not board.turn
        capture_mask = board.occupied_co[enemy_color]
        if board.ep_square:
            capture_mask |= (1 << board.ep_square)
        moves = board.generate_legal_moves(chess.BB_ALL, capture_mask)

        for move in moves:
            board.push(move)
            score = -self.quiescence(board, -beta, -alpha)
            board.pop()

            if score >= beta:
                return beta
            if score > best_value:
                best_value = score
            if score > alpha:
                alpha = score
        return best_value
