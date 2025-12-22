import pygame, sys
from game_logic import TicTacToe
from ai_engine import GameAI
from performance import run_analysis_graph

TEAL, WHITE, BLACK, PANEL_BG = (28, 170, 156), (255, 255, 255), (0, 0, 0), (45, 52, 54)
GREEN, RED, SELECTED = (46, 204, 113), (231, 76, 60), (241, 196, 15)
WIDTH, HEIGHT, BOARD_SIZE = 950, 600, 600

class GameGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic-Tac-Toe: Algoritma Kapışması")
        self.font = pygame.font.SysFont('arial', 15, bold=True)
        self.title_font = pygame.font.SysFont('arial', 40, bold=True)
        self.result_font = pygame.font.SysFont('arial', 50, bold=True)
        self.grid_size = 3
        self.reset_game()
        self.state = "MENU"

    def reset_game(self):
        self.game = TicTacToe(self.grid_size)
        self.ai = GameAI(self.game)
        self.sq_size = BOARD_SIZE // self.grid_size
        self.last_stats = {"time": 0, "ab_nodes": 0, "mm_nodes": 0, "depth": 0}

    def draw_button(self, text, x, y, w, h, color):
        m = pygame.mouse.get_pos(); click = pygame.mouse.get_pressed()
        over = x < m[0] < x+w and y < m[1] < y+h
        pygame.draw.rect(self.screen, color if not over else WHITE, (x, y, w, h), border_radius=8)
        txt = self.font.render(text, True, BLACK)
        self.screen.blit(txt, txt.get_rect(center=(x+w/2, y+h/2)))
        return over and click[0]

    def draw_board(self):
        pygame.draw.rect(self.screen, PANEL_BG, (0, 0, BOARD_SIZE, BOARD_SIZE))
        for i in range(1, self.grid_size):
            pygame.draw.line(self.screen, BLACK, (0, i*self.sq_size), (BOARD_SIZE, i*self.sq_size), 4)
            pygame.draw.line(self.screen, BLACK, (i*self.sq_size, 0), (i*self.sq_size, BOARD_SIZE), 4)
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                mid = (c*self.sq_size+self.sq_size//2, r*self.sq_size+self.sq_size//2)
                if self.game.board[r,c] == 1:
                    p = self.sq_size//4
                    pygame.draw.line(self.screen, WHITE, (mid[0]-p, mid[1]-p), (mid[0]+p, mid[1]+p), 8)
                    pygame.draw.line(self.screen, WHITE, (mid[0]-p, mid[1]+p), (mid[0]+p, mid[1]-p), 8)
                elif self.game.board[r,c] == 2:
                    pygame.draw.circle(self.screen, RED, mid, self.sq_size//4, 8)

    def run(self):
        while True:
            self.screen.fill(PANEL_BG)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if self.state == "PLAYING" and self.game.current_player == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                    if event.pos[0] < BOARD_SIZE:
                        r, c = event.pos[1]//self.sq_size, event.pos[0]//self.sq_size
                        if self.game.make_move((r, c)):
                            if self.game.is_terminal(): self.state = "GAMEOVER"
                            else: self.game.current_player = 2

            if self.state == "MENU":
                title = self.title_font.render("XOX ANALİZ MOTORU", True, WHITE)
                self.screen.blit(title, (WIDTH//2-title.get_width()//2, 80))
                
                # --- SADECE 3x3 ve 4x4 SECENEKLERİ ---
                for i, s in enumerate([3, 4]):
                    # Butonları ortalamak için X koordinatı ayarlandı
                    if self.draw_button(f"{s}x{s}", WIDTH//2-105+i*110, 240, 100, 50, SELECTED if self.grid_size==s else WHITE):
                        self.grid_size = s; self.reset_game()
                
                if self.draw_button("OYUNA BASLA", WIDTH//2-125, 380, 250, 60, GREEN):
                    self.reset_game(); self.state = "PLAYING"; pygame.time.wait(200)

            elif self.state in ["PLAYING", "GAMEOVER"]:
                self.draw_board()
                y_p = 40
                self.screen.blit(self.font.render(f"MOD: {self.grid_size}x{self.grid_size} | DERINLIK: {self.last_stats['depth']}", True, SELECTED), (BOARD_SIZE+30, y_p))
                y_p += 50
                pygame.draw.rect(self.screen, RED, (BOARD_SIZE+25, y_p, 300, 80), 2, border_radius=5)
                self.screen.blit(self.font.render("MINIMAX (Saf)", True, RED), (BOARD_SIZE+35, y_p+10))
                self.screen.blit(self.font.render(f"Gezilen Dugum: {self.last_stats['mm_nodes']}", True, WHITE), (BOARD_SIZE+35, y_p+40))
                y_p += 100
                pygame.draw.rect(self.screen, GREEN, (BOARD_SIZE+25, y_p, 300, 100), 2, border_radius=5)
                self.screen.blit(self.font.render("ALPHA-BETA (Budama)", True, GREEN), (BOARD_SIZE+35, y_p+10))
                self.screen.blit(self.font.render(f"Gezilen Dugum: {self.last_stats['ab_nodes']}", True, WHITE), (BOARD_SIZE+35, y_p+40))
                saved = max(0, self.last_stats['mm_nodes'] - self.last_stats['ab_nodes'])
                self.screen.blit(self.font.render(f"Budanan Dal: {saved}", True, SELECTED), (BOARD_SIZE+35, y_p+70))

                if self.state == "PLAYING" and self.game.current_player == 2:
                    pygame.display.flip()
                    pygame.time.wait(500)
                    move, t, ab_n, mm_n, d = self.ai.get_comparison_data(0.8)
                    self.last_stats = {"time": t, "ab_nodes": ab_n, "mm_nodes": mm_n, "depth": d}
                    if move: self.game.make_move(move)
                    if self.game.is_terminal(): self.state = "GAMEOVER"
                    else: self.game.current_player = 1

                if self.state == "GAMEOVER":
                    for p in [1, 2]:
                        coords = self.game.get_winner_coords(p)
                        if coords:
                            s = (coords[0][1]*self.sq_size + self.sq_size//2, coords[0][0]*self.sq_size + self.sq_size//2)
                            e = (coords[-1][1]*self.sq_size + self.sq_size//2, coords[-1][0]*self.sq_size + self.sq_size//2)
                            pygame.draw.line(self.screen, WHITE, s, e, 10)
                    overlay = pygame.Surface((BOARD_SIZE, BOARD_SIZE), pygame.SRCALPHA); overlay.fill((0, 0, 0, 200))
                    self.screen.blit(overlay, (0, 0))
                    if self.game.check_winner(1): msg = "TEBRİKLER!"
                    elif self.game.check_winner(2): msg = "AI KAZANDI!"
                    else: msg = "BERABERE!"
                    txt = self.result_font.render(msg, True, WHITE)
                    self.screen.blit(txt, txt.get_rect(center=(BOARD_SIZE//2, BOARD_SIZE//2-50)))
                    if self.draw_button("GRAFİK ANALİZİ", BOARD_SIZE//2-150, BOARD_SIZE//2+40, 300, 50, SELECTED):
                        run_analysis_graph(self.grid_size, min(self.last_stats['depth']+1, 6))
                        self.state = "MENU"
                    if self.draw_button("ANA MENÜ", BOARD_SIZE//2-150, BOARD_SIZE//2+105, 300, 50, WHITE): self.state = "MENU"

            pygame.display.flip()

def start_game(): GameGUI().run()