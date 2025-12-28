import numpy as np

class TicTacToe:
    def __init__(self, size=3):
        """
        Tic-Tac-Toe oyununun temel yapısını oluşturur.
        - size: Tahtanın boyutu (burada sabit 3x3).
        - board: Oyun alanını temsil eden 0'lardan oluşan bir matris (0: Boş, 1: İnsan, 2: AI).
        - current_player: Hamle sırasının kimde olduğunu takip eder.
        """
        self.size = 3 
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        
    def reset(self):
        #Yeni bir oyun için tahtayı temizler ve sırayı insana (1) verir.
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1
        
    def get_valid_moves(self):
        #Tahta taranır ve henüz doldurulmamış (değeri 0 olan) koordinatlar liste olarak döndürülür.
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == 0]
    
    def make_move(self, move):
        """
        Gelen koordinata (satır, sütun) mevcut oyuncunun işareti koyulur.
        Eğer seçilen yer doluysa 'False', başarılıysa 'True' döndürülür.
        """
        row, col = move
        if self.board[row][col] == 0:
            self.board[row][col] = self.current_player
            return True
        return False
    
    def check_winner(self, player):
        # Belirtilen oyuncunun kazanıp kazanmadığı kontrol edilir
        return self.get_winner_coords(player) is not None

    def get_winner_coords(self, player):
        """
        Kazanma durumları 4 farklı açıda kontrol edilir:
        1. Yatay: Herhangi bir satır tamamen oyuncunun taşlarıyla mı dolu?
        2. Dikey: Herhangi bir sütun tamamen oyuncunun taşlarıyla mı dolu?
        3. Köşegen 1: Sol üstten sağ alta çapraz dolu mu?
        4. Köşegen 2: Sağ üstten sol alta çapraz dolu mu?
        """
        for r in range(3):
            if all(self.board[r, :] == player): return [(r, c) for c in range(3)]
        for c in range(3):
            if all(self.board[:, c] == player): return [(r, c) for r in range(3)]
        if all(np.diag(self.board) == player): return [(i, i) for i in range(3)]
        if all(np.diag(np.fliplr(self.board)) == player): return [(i, 3 - 1 - i) for i in range(3)]
        return None

    def is_terminal(self):
        """Oyunun bitip bitmediği kontrol edilir: Biri kazandıysa veya hiç boş yer kalmadıysa oyun biter."""
        return self.check_winner(1) or self.check_winner(2) or len(self.get_valid_moves()) == 0
        
    def evaluate(self, depth):
        """
        Yapay zekanın 'sezgisel' değerlendirme fonksiyonu. 
        Oyun henüz bitmediyse bile mevcut tahtaya bir puan verilir:
        - Pozitif Puan: Yapay zeka avantajlı.
        - Negatif Puan: İnsan oyuncu avantajlı.
        - 'depth' (derinlik) eklenmesi: AI'nın en kısa yoldan kazanmayı seçmesini sağlar.
        """
        if self.check_winner(2): return 100 + depth # AI kazandı (Harika!)
        if self.check_winner(1): return -100 - depth # İnsan kazandı (Kötü!)
        
        score = 0
        lines = []
        # Tahtadaki tüm olası kazanma hatları (satır, sütun, çapraz)
        for i in range(3):
            lines.append(list(self.board[i, :]))
            lines.append(list(self.board[:, i]))
        lines.append(list(np.diag(self.board)))
        lines.append(list(np.diag(np.fliplr(self.board))))
        
        # Her hat için sezgisel puanlama
        for line in lines:
            ai_c, hum_c, empty_c = line.count(2), line.count(1), line.count(0)
            # İnsan oyuncunun kazanma tehdidi
            if hum_c == 2 and empty_c == 1: score -= 50 
            # Yapay zekâ için kazanma fırsatı
            if ai_c == 2 and empty_c == 1: score += 20    
        
        return score