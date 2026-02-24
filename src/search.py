import chess
from src.evals import evaluate_board
from src.tt import TT
import time

# for benchmarking purposes count node computation for search
class Search:
    def __init__(self):
        # transposition table
        self.tt = TT()
        self.nodes = 0
        self.stop_flag = False
        self.start_time = 0
        self.time_limit = 0
        self.killers = [[None]*2 for _ in range(64)]
        self.history = [[0]*64 for _ in range(64)]

    def start_search(self, board, time_limit=5.0):
        self.stop_flag = False
        self.nodes = 0
        self.start_time = time.time()
        self.time_limit = time_limit

        best_move = None

        for depth in range(1,100):
            score, move = self.negamax(board, -float('inf'), float('inf'), depth, 0 )
            if self.stop_flag:
                break

            best_move = move

            print(f"info depth {depth} score cp {score} nodes {self.nodes} pv {best_move}")

            if self.check_time():
              break

        return best_move

    def negamax(self, board:chess.Board, alpha:float, beta:float, depth:int, ply:int):
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
        if self.nodes & 2047 == 0:
            self.check_time()

        if self.stop_flag:
            return 0, None

        self.nodes += 1

        key = hash(board.fen())
        tt_entry = self.tt.probe(key)
        tt_move = None

        if tt_entry:
            tt_move = tt_entry['move']
            if tt_entry['depth'] >= depth:
                if tt_entry['flag'] == self.tt.EXACT:
                    return tt_entry['score'], tt_entry['move']
                if tt_entry['flag'] == self.tt.LOWERBOUND:
                    alpha = max(alpha, tt_entry['score'])
                elif tt_entry['flag'] == self.tt.UPPERBOUND:
                    beta = min(beta, tt_entry['score'])
                if alpha >= beta:
                    return tt_entry['score'], tt_entry['move']

        if depth == 0:
            return self.quiescence(board, alpha, beta), None

        if board.is_game_over():
            if board.is_checkmate():
                return -100000 + ply, None
            else:
                return 0, None

        def score_move(move):
            if move == tt_move:
                return 2000000

            if board.is_capture(move):
                return 1000000

            if move == self.killers[ply][0]:
                return 90000
            if move == self.killers[ply][1]:
                return 800000

            return self.history[move.from_square][move.to_square]

        moves = list(board.legal_moves)
        moves.sort(key=score_move, reverse=True)

        best_move = None
        current_flag = self.tt.UPPERBOUND

        for move in moves:
            board.push(move)
            score, _ = self.negamax(board, -beta, -alpha, depth-1, ply + 1)
            score = -score
            board.pop()

            if self.stop_flag:
                return 0, None
            if score >= beta:
                if not board.is_capture(move):
                    if move != self.killers[ply][0]:
                        self.killers[ply][1] = self.killers[ply][0]
                        self.killers[ply][0] = move

                    bonus = depth * depth
                    self.history[move.from_square][move.to_square] += bonus

                self.tt.store(key, depth, beta, self.tt.LOWERBOUND, move)
                return beta, move

            if score > alpha:
                alpha = score
                best_move = move
                current_flag = self.tt.EXACT

        if best_move is None:
            self.tt.store(key, depth, alpha, self.tt.UPPERBOUND, None)
        else:
            self.tt.store(key, depth, alpha, current_flag, best_move)

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

    def check_time(self):
        if time.time() - self.start_time > self.time_limit:
            self.stop_flag = True
        return self.stop_flag
