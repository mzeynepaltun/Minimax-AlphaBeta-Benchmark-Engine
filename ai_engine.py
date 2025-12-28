import time

class GameAI:
    def __init__(self, game):
        """Yapay zeka motoru, oyunun kuralları için 'game' objesini kullanır."""
        self.game = game
        self.nodes_visited = 0 
        # Performans ölçümü için ziyaret edilen düğüm (tahta durumu) sayısı

    def _order_moves(self, moves):
        """
        Hamle Sıralama: Merkeze yakın hamleleri önce değerlendirir. 
        Tic-Tac-Toe oyununda orta kare stratejik olarak daha güçlü olduğu için
        bu sıralama Alpha-Beta Budaması'nın daha erken ve daha etkili çalışmasını sağlar.
        """
        center = self.game.size / 2
        return sorted(moves, key=lambda m: (abs(m[0]-center) + abs(m[1]-center)))

    def alpha_beta(self, depth, alpha, beta, is_maximizing, start_time, time_limit):
        """
        Alpha-Beta Budaması algoritması.
        - depth: Kaç hamle sonrasını hayal ediyorum?
        - alpha: AI'nın garantilediği en iyi puan (Aşağısı kurtarmaz).
        - beta: İnsanın AI'ya verebileceği en kötü puan (Yukarıya izin vermez).
        """
        # Zaman sınırı aşılırsa aramayı durdurur (oyun donmasını engeller)
        if time.perf_counter() - start_time > time_limit: return None, None
        
        self.nodes_visited += 1 
        
        # Kazanma durumları kontrol edilir
        if self.game.check_winner(2): return 100 + depth, None
        if self.game.check_winner(1): return -100 - depth, None
        
        valid_moves = self.game.get_valid_moves()
        # Derinlik bittiğinde veya hamle kalmadığında tahtanın puanı hesaplanır
        if len(valid_moves) == 0 or depth == 0: return self.game.evaluate(depth), None
        
        # Hamleler stratejik sıraya sokulur        
        ordered_moves = self._order_moves(valid_moves)
        best_move = ordered_moves[0]
        
        """ MAX (AI)"""
        if is_maximizing: # AI'nın hamlesi simüle edilir, en yüksek puan aranır.
            max_eval = float('-inf')
            for move in ordered_moves:
                self.game.board[move[0]][move[1]] = 2 # Hamle yapılır
                # Rakip oyuncunun (insan) hamlesi simüle edilir
                eval_score, _ = self.alpha_beta(depth - 1, alpha, beta, False, start_time, time_limit)
                self.game.board[move[0]][move[1]] = 0 # Tahtayı eski haline getirilir
                
                # Zaman aşımı varsa üst seviyeye çık                
                if eval_score is None: return None, None
                # En iyi skor güncellenir
                if eval_score > max_eval: max_eval, best_move = eval_score, move
                
                #Alfa güncellenir                
                alpha = max(alpha, eval_score)
                
                if beta <= alpha: break 
                # BUDAMA İŞLEMİ
                
            return max_eval, best_move
            
        """ MIN (İnsan)"""   
        else: # İnsan oyuncunun hamlesi simüle edilir, en düşük puan aranır.
            min_eval = float('inf')
            for move in ordered_moves:
                self.game.board[move[0]][move[1]] = 1
                eval_score, _ = self.alpha_beta(depth - 1, alpha, beta, True, start_time, time_limit)
                self.game.board[move[0]][move[1]] = 0
                
                if eval_score is None: return None, None
                if eval_score < min_eval: min_eval, best_move = eval_score, move
                
                beta = min(beta, eval_score)
                if beta <= alpha: break # BUDAMA İŞLEMİ
            return min_eval, best_move

    def minimax_only_nodes(self, depth, is_maximizing):
        """
        Minimax algoritması.
        Hiçbir budama yapmadan tüm olası hamleleri inceler.
        Bu fonksiyon, Alpha-Beta Budaması ile karşılaştırma yapabilmek
        için yalnızca ziyaret edilen düğüm sayısını ölçmek amacıyla kullanılır.
        """
        self.nodes_visited += 1
        if self.game.check_winner(2) or self.game.check_winner(1) or depth == 0: return
        
        valid_moves = self.game.get_valid_moves()
        for move in valid_moves:
            self.game.board[move[0]][move[1]] = (2 if is_maximizing else 1)
            self.minimax_only_nodes(depth - 1, not is_maximizing)
            self.game.board[move[0]][move[1]] = 0

    def get_comparison_data(self, time_limit=0.8):
        """
        Gerçek zamanlı karşılaştırma verisi toplar. 
        - Alpha-Beta algoritması iterative deepening ile derinliği artırarak çalıştırılır.
        - Aynı derinlikte saf Minimax'ın ziyaret ettiği düğüm sayısı hesaplanır.
        """
        start_time = time.perf_counter()
        last_move, d = None, 1
        ab_nodes = 0
        
        while d < 10: # Maksimum derinlik sınırı
            self.nodes_visited = 0
            res, move = self.alpha_beta(d, float('-inf'), float('inf'), True, start_time, time_limit)
            if move is None: break 
            last_move, ab_nodes, d = move, self.nodes_visited, d + 1
            # Kazanma durumu netleştiyse daha derine inmemesi sağlanır
            if res > 90 or res < -90: break 
            
        final_depth = d - 1
        # Aynı derinlikte saf Minimax çalıştırılır
        self.nodes_visited = 0
        self.minimax_only_nodes(final_depth, True) # Kıyaslama verisi üretilir
        
        return last_move, time.perf_counter()-start_time, ab_nodes, self.nodes_visited, final_depth