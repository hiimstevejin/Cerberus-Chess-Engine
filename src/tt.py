class TT:
    def __init__(self, size_mb=64):
        self.table = {}
        self.EXACT = 0
        self.LOWERBOUND = 1
        self.UPPERBOUND = 2

    def probe(self, key):
        return self.table.get(key)

    def store(self, key, depth, score, flag, move):
        self.table[key] = {
                  'depth': depth,
                  'score': score,
                  'flag': flag,
                  'move': move
              }
