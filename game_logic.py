import numpy as np

class TicTacToe:
    def __init__(self, size=3):
        self.size = 3 
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        
    def reset(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        
    def get_valid_moves(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == 0]
    
    def make_move(self, move):
        row, col = move
        if self.board[row][col] == 0:
            self.board[row][col] = self.current_player
            return True
        return False
    
    def check_winner(self, player):
        return self.get_winner_coords(player) is not None

    def get_winner_coords(self, player):
        for r in range(3):
            if all(self.board[r, :] == player): return [(r, c) for c in range(3)]
        for c in range(3):
            if all(self.board[:, c] == player): return [(r, c) for r in range(3)]
        if all(np.diag(self.board) == player): return [(i, i) for i in range(3)]
        if all(np.diag(np.fliplr(self.board)) == player): return [(i, 3 - 1 - i) for i in range(3)]
        return None

    def is_terminal(self):
        return self.check_winner(1) or self.check_winner(2) or len(self.get_valid_moves()) == 0
        
    def evaluate(self, depth):
        if self.check_winner(2): return 100 + depth
        if self.check_winner(1): return -100 - depth
        
        score = 0
        lines = []
        for i in range(3):
            lines.append(list(self.board[i, :]))
            lines.append(list(self.board[:, i]))
        lines.append(list(np.diag(self.board)))
        lines.append(list(np.diag(np.fliplr(self.board))))

        for line in lines:
            ai_c, hum_c, empty_c = line.count(2), line.count(1), line.count(0)
            if hum_c == 2 and empty_c == 1: score -= 50 
            if ai_c == 2 and empty_c == 1: score += 20    
        
        # Merkez kontrolü kaldırıldı.
        return score