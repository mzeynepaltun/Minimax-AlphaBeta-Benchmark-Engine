import numpy as np

class TicTacToe:
    def __init__(self, size=3):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.current_player = 1
        
    def reset(self):
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.current_player = 1
        
    def get_valid_moves(self):
        return [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == 0]
    
    def make_move(self, move):
        row, col = move
        if self.board[row][col] == 0:
            self.board[row][col] = self.current_player
            return True
        return False
    
    def check_winner(self, player):
        return self.get_winner_coords(player) is not None

    def get_winner_coords(self, player):
        # Satırlar
        for r in range(self.size):
            if all(self.board[r, :] == player):
                return [(r, c) for c in range(self.size)]
        # Sütunlar
        for c in range(self.size):
            if all(self.board[:, c] == player):
                return [(r, c) for r in range(self.size)]
        # Çaprazlar
        if all(np.diag(self.board) == player):
            return [(i, i) for i in range(self.size)]
        if all(np.diag(np.fliplr(self.board)) == player):
            return [(i, self.size - 1 - i) for i in range(self.size)]
        return None

    def is_terminal(self):
        return self.check_winner(1) or self.check_winner(2) or len(self.get_valid_moves()) == 0
        
    def evaluate(self, depth):
        if self.check_winner(2): return 100 + depth
        if self.check_winner(1): return -100 - depth
        
        score = 0
        lines = []
        for i in range(self.size):
            lines.append(list(self.board[i, :]))
            lines.append(list(self.board[:, i]))
        lines.append(list(np.diag(self.board)))
        lines.append(list(np.diag(np.fliplr(self.board))))

        for line in lines:
            ai_c, hum_c, empty_c = line.count(2), line.count(1), line.count(0)
            if hum_c == (self.size - 1) and empty_c == 1: score -= 50 # Savunma
            if ai_c == (self.size - 1) and empty_c == 1: score += 20    # Saldırı

        center = self.size // 2
        if self.board[center, center] == 2: score += 5
        return score
