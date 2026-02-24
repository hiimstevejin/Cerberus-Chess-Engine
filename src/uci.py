import sys
import chess
import threading
from src.search import Search

class UCI:
    def __init__(self):
        self.board = chess.Board()
        self.search = Search()
        self.search_thread = None

    def uci_loop(self):
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break

                command = line.strip()
                self.handle_command(command)

            except Exception as e:
                with open("debug.log", "a") as f:
                    f.write(f"Error: {e}\n")

    def handle_command(self, command):
        parts = command.split()
        if not parts:
            return

        cmd = parts[0]

        if cmd == "uci":
            print("id name hiimstevejin^^")
            print("id hiimstevejin")
            print("option name Hash type spin default 128 min 1 max 1024")
            print("option name Threads type spin default 1 min 1 max 8")
            print("option name Move Overhead type spin default 100 min 0 max 10000")
            print("uciok")
            sys.stdout.flush()

        elif cmd == "isready":
            print("readyok")
            sys.stdout.flush()

        elif cmd == "ucinewgame":
            self.search.tt.table.clear()
            self.search.killers = [[None]*2 for _ in range(64)]
            self.search.history = [[0]*64 for _ in range(64)]

        elif cmd == "position":
            self.parse_position(parts)

        elif cmd == "go":
            self.parse_go(parts)

        elif cmd == "stop":
            self.search.stop_flag = True

        elif cmd == "quit":
            sys.exit()

    def parse_position(self, parts):

        move_idx = 0

        if parts[1] == "startpos":
            self.board.reset()
            move_idx = 2
        elif parts[1] == "fen":
            fen_parts = []
            move_idx = 2
            for i in range(2, len(parts)):
                if parts[i] == "moves":
                    move_idx = i
                    break
                fen_parts.append(parts[i])

            fen = " ".join(fen_parts)
            self.board.set_fen(fen)

        if move_idx < len(parts) and parts[move_idx] == "moves":
            for move_str in parts[move_idx+1:]:
                self.board.push_uci(move_str)

    def parse_go(self, parts):

        time_limit = 5.0

        try:
            if "movetime" in parts:
                idx = parts.index("movetime")
                ms = int(parts[idx+1])
                time_limit = ms / 1000.0

            elif "wtime" in parts:
                idx_w = parts.index("wtime")
                idx_b = parts.index("btime")
                wtime = int(parts[idx_w])
                btime = int(parts[idx_b])

                if self.board.turn == chess.WHITE:
                    time_limit = (wtime / 30) / 1000.0
                else:
                    time_limit = (btime / 30) / 1000.0

                if time_limit < 0.1:
                    time_limit = 0.1

        except ValueError:
            pass

        self.search_thread = threading.Thread(
            target=self.run_search,
            args=(time_limit,)
        )
        self.search_thread.start()

    def run_search(self, time_limit):
        best_move = self.search.start_search(self.board, time_limit)
        print(f"bestmove {best_move}")
        sys.stdout.flush()
