import time

class GameAI:
    def __init__(self, game):
        self.game = game
        self.nodes_visited = 0
        self.total_possible_nodes = 0

    def _order_moves(self, moves):
        center = self.game.size / 2
        return sorted(moves, key=lambda m: (abs(m[0]-center) + abs(m[1]-center)))

    def alpha_beta(self, depth, alpha, beta, is_maximizing, start_time, time_limit):
        if time.perf_counter() - start_time > time_limit:
            return None, None
        self.nodes_visited += 1
        
        if self.game.check_winner(2): return 100 + depth, None
        if self.game.check_winner(1): return -100 - depth, None
        valid_moves = self.game.get_valid_moves()
        if len(valid_moves) == 0 or depth == 0: return self.game.evaluate(depth), None
        
        ordered_moves = self._order_moves(valid_moves)
        best_move = ordered_moves[0]
        if is_maximizing:
            max_eval = float('-inf')
            for move in ordered_moves:
                self.game.board[move[0]][move[1]] = 2
                eval_score, _ = self.alpha_beta(depth - 1, alpha, beta, False, start_time, time_limit)
                self.game.board[move[0]][move[1]] = 0
                if eval_score is None: return None, None
                if eval_score > max_eval: max_eval, best_move = eval_score, move
                alpha = max(alpha, eval_score)
                if beta <= alpha: break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in ordered_moves:
                self.game.board[move[0]][move[1]] = 1
                eval_score, _ = self.alpha_beta(depth - 1, alpha, beta, True, start_time, time_limit)
                self.game.board[move[0]][move[1]] = 0
                if eval_score is None: return None, None
                if eval_score < min_eval: min_eval, best_move = eval_score, move
                beta = min(beta, eval_score)
                if beta <= alpha: break
            return min_eval, best_move

    def minimax_only_nodes(self, depth, is_maximizing):
        """Sadece karşılaştırma amaçlı düğüm sayar."""
        self.nodes_visited += 1
        if self.game.check_winner(2) or self.game.check_winner(1) or depth == 0:
            return
        valid_moves = self.game.get_valid_moves()
        for move in valid_moves:
            self.game.board[move[0]][move[1]] = (2 if is_maximizing else 1)
            self.minimax_only_nodes(depth - 1, not is_maximizing)
            self.game.board[move[0]][move[1]] = 0

    def get_comparison_data(self, time_limit=0.8):
        # 1. Alpha-Beta ile en iyi hamleyi bul (Iterative Deepening)
        start_time = time.perf_counter()
        last_move, d = None, 1
        ab_nodes = 0
        while d < 12:
            self.nodes_visited = 0
            res, move = self.alpha_beta(d, float('-inf'), float('inf'), True, start_time, time_limit)
            if move is None: break
            last_move, ab_nodes, d = move, self.nodes_visited, d + 1
            if res > 90 or res < -90: break
        
        final_depth = d - 1
        # 2. Aynı derinlikte Minimax ne kadar düğüm gezerdi?
        self.nodes_visited = 0
        self.minimax_only_nodes(final_depth, True)
        mm_nodes = self.nodes_visited
        
        return last_move, time.perf_counter()-start_time, ab_nodes, mm_nodes, final_depth
