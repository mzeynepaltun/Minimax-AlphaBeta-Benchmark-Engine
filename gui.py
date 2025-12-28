import pygame, sys
from game_logic import TicTacToe
from ai_engine import GameAI
from performance import run_analysis_graph

# Uygulamada kullanılacak renklerin RGB kodları
TEAL, WHITE, BLACK, PANEL_BG = (28, 170, 156), (255, 255, 255), (0, 0, 0), (45, 52, 54)
GREEN, RED, SELECTED = (46, 204, 113), (231, 76, 60), (241, 196, 15)
WIDTH, HEIGHT, BOARD_SIZE = 950, 600, 600

class GameGUI:
    def __init__(self):
        """Pencereyi başlatır, başlığı ayarlar ve fontları yükler."""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic-Tac-Toe: Algoritma Analizi")
        # Yazı tipleri
        self.font = pygame.font.SysFont('arial', 15, bold=True)
        self.title_font = pygame.font.SysFont('arial', 40, bold=True)
        self.result_font = pygame.font.SysFont('arial', 50, bold=True)
        self.grid_size = 3
        self.reset_game()
        self.state = "MENU" # Oyunun hangi ekranda olduğu: MENU, PLAYING veya GAMEOVER

    def reset_game(self):
        """Oyun bittiğinde her şeyi temizleyip baştan başlatmak için kullanılır."""
        self.game = TicTacToe(3)
        self.ai = GameAI(self.game)
        self.sq_size = BOARD_SIZE // 3
        self.last_stats = {"time": 0, "ab_nodes": 0, "mm_nodes": 0, "depth": 0}

    def draw_button(self, text, x, y, w, h, color):
        """
        Özel bir buton çizici. 
        - Fare butona değdiğinde (hover) rengi beyaza döner.
        - Tıklanırsa 'True' döndürür, böylece ana döngüde karar verilebilir.
        """
        m = pygame.mouse.get_pos(); click = pygame.mouse.get_pressed()
        over = x < m[0] < x+w and y < m[1] < y+h
        pygame.draw.rect(self.screen, color if not over else WHITE, (x, y, w, h), border_radius=8)
        txt = self.font.render(text, True, BLACK)
        self.screen.blit(txt, txt.get_rect(center=(x+w/2, y+h/2)))
        return over and click[0]

    def draw_board(self):
        """Oyun tahtasını (ızgara ve taşlar) ekrana çizer."""
        pygame.draw.rect(self.screen, PANEL_BG, (0, 0, BOARD_SIZE, BOARD_SIZE))
        # Çizgileri çiz
        for i in range(1, 3):
            pygame.draw.line(self.screen, BLACK, (0, i*self.sq_size), (BOARD_SIZE, i*self.sq_size), 4)
            pygame.draw.line(self.screen, BLACK, (i*self.sq_size, 0), (i*self.sq_size, BOARD_SIZE), 4)
        
        # Taşları (X ve O) çiz
        for r in range(3):
            for c in range(3):
                mid = (c*self.sq_size+self.sq_size//2, r*self.sq_size+self.sq_size//2)
                if self.game.board[r,c] == 1: # Oyuncu (Beyaz X)
                    p = self.sq_size//4
                    pygame.draw.line(self.screen, WHITE, (mid[0]-p, mid[1]-p), (mid[0]+p, mid[1]+p), 8)
                    pygame.draw.line(self.screen, WHITE, (mid[0]-p, mid[1]+p), (mid[0]+p, mid[1]-p), 8)
                elif self.game.board[r,c] == 2: # Yapay Zeka (Kırmızı Daire)
                    pygame.draw.circle(self.screen, RED, mid, self.sq_size//4, 8)

    def run(self):
        """Oyunun ana kalbi. Saniyede defalarca döner ve olayları (tıklama vb.) kontrol eder."""
        while True:
            self.screen.fill(PANEL_BG) # Ekranı her karede temizle
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                
                # İnsan hamlesi: Sıra bizdeyse ve tahtaya tıkladıysak
                if self.state == "PLAYING" and self.game.current_player == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] < BOARD_SIZE:
                        r, c = event.pos[1]//self.sq_size, event.pos[0]//self.sq_size
                        if self.game.make_move((r, c)):
                            if self.game.is_terminal(): self.state = "GAMEOVER"
                            else: self.game.current_player = 2 # Sırayı AI'ya ver

            # --- EKRAN DURUMLARINA GÖRE GÖRÜNTÜLEME ---
            if self.state == "MENU":
                title = self.title_font.render("TIC-TAC-TOE", True, WHITE)
                self.screen.blit(title, (WIDTH//2-title.get_width()//2, 150))
                if self.draw_button("OYUNA BAŞLA", WIDTH//2-125, 300, 250, 60, GREEN):
                    self.reset_game(); self.state = "PLAYING"; pygame.time.wait(200)

            elif self.state in ["PLAYING", "GAMEOVER"]:
                self.draw_board()
                
                # Sağ Panel: İstatistikleri yazdır
                y_p = 40
                self.screen.blit(self.font.render(f"MOD: 3x3 | DERİNLİK: {self.last_stats['depth']}", True, SELECTED), (BOARD_SIZE+30, y_p))
                
                # Saf Minimax istatistiği (Kırmızı kutu)
                y_p += 50
                pygame.draw.rect(self.screen, RED, (BOARD_SIZE+25, y_p, 300, 80), 2, border_radius=5)
                self.screen.blit(self.font.render("MINIMAX", True, RED), (BOARD_SIZE+35, y_p+10))
                self.screen.blit(self.font.render(f"Gezilen Düğüm: {self.last_stats['mm_nodes']}", True, WHITE), (BOARD_SIZE+35, y_p+40))
                
                # Alpha-Beta istatistiği (Yeşil kutu)
                y_p += 100
                pygame.draw.rect(self.screen, GREEN, (BOARD_SIZE+25, y_p, 300, 100), 2, border_radius=5)
                self.screen.blit(self.font.render("ALPHA-BETA", True, GREEN), (BOARD_SIZE+35, y_p+10))
                self.screen.blit(self.font.render(f"Gezilen Düğüm: {self.last_stats['ab_nodes']}", True, WHITE), (BOARD_SIZE+35, y_p+40))
                
                # Budama işleminde ne kadar düğümü analiz etmeden elediğini gösterir.
                saved = max(0, self.last_stats['mm_nodes'] - self.last_stats['ab_nodes'])
                self.screen.blit(self.font.render(f"Budanan Dal: {saved}", True, SELECTED), (BOARD_SIZE+35, y_p+70))

                # Yapay Zeka Sırası: AI karar verir ve istatistikleri günceller
                if self.state == "PLAYING" and self.game.current_player == 2:
                    pygame.display.flip(); pygame.time.wait(500)
                    move, t, ab_n, mm_n, d = self.ai.get_comparison_data(0.8)
                    self.last_stats = {"time": t, "ab_nodes": ab_n, "mm_nodes": mm_n, "depth": d}
                    if move: self.game.make_move(move)
                    if self.game.is_terminal(): self.state = "GAMEOVER"
                    else: self.game.current_player = 1

                # Oyun Sonu: Kazananı gösterir ve analiz grafiğine gitme seçeneği sunar
                if self.state == "GAMEOVER":
                    overlay = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA); overlay.fill((0, 0, 0, 200))
                    self.screen.blit(overlay, (0, 0))
                    msg = "TEBRİKLER!" if self.game.check_winner(1) else "AI KAZANDI!" if self.game.check_winner(2) else "BERABERE!"
                    txt = self.result_font.render(msg, True, WHITE)
                    self.screen.blit(txt, txt.get_rect(center=(BOARD_SIZE//2, BOARD_SIZE//2-50)))
                    if self.draw_button("GRAFİK ANALİZİ (6 DERİNLİK)", BOARD_SIZE//2-150, BOARD_SIZE//2+40, 300, 50, SELECTED):
                        run_analysis_graph(3, 6)
                        self.state = "MENU"
                    if self.draw_button("ANA MENÜ", BOARD_SIZE//2-150, BOARD_SIZE//2+105, 300, 50, WHITE): self.state = "MENU"

            pygame.display.flip()

def start_game(): GameGUI().run()