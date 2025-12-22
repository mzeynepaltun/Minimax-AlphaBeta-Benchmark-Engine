import matplotlib.pyplot as plt
import os, psutil, time
from game_logic import TicTacToe
from ai_engine import GameAI

def get_memory_usage():
    try: return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
    except: return 0

def run_analysis_graph(grid_size=3, max_depth=6): 
    depths = list(range(1, max_depth + 1))
    res = {'minimax': {'t': [], 'n': [], 'm': []}, 'alphabeta': {'t': [], 'n': [], 'm': []}}
    
    for d in depths:
        for method in ['minimax', 'alphabeta']:
            m_start = get_memory_usage()
            g = TicTacToe(3); ai = GameAI(g)
            
            start = time.perf_counter()
            if method == 'minimax': 
                ai.minimax_only_nodes(d, True)
            else: 
                ai.alpha_beta(d, float('-inf'), float('inf'), True, time.perf_counter(), 20.0)
            t = time.perf_counter() - start
            
            res[method]['t'].append(t)
            res[method]['n'].append(ai.nodes_visited)
            res[method]['m'].append(max(0.01, get_memory_usage() - m_start))

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle(f"3x3 Tahta - {max_depth} Derinlik Performans Analizi")
    ax1.plot(depths, res['minimax']['t'], 'r-o', label='Minimax'); ax1.plot(depths, res['alphabeta']['t'], 'b-s', label='Alpha-Beta')
    ax1.set_title('Süre (sn)'); ax1.legend()
    ax2.plot(depths, res['minimax']['n'], 'r-o', label='Minimax'); ax2.plot(depths, res['alphabeta']['n'], 'b-s', label='Alpha-Beta')
    ax2.set_yscale('log'); ax2.set_title('Düğüm Sayısı (Log)'); ax2.legend()
    ax3.plot(depths, res['minimax']['m'], 'r-o', label='Minimax'); ax3.plot(depths, res['alphabeta']['m'], 'b-s', label='Alpha-Beta')
    ax3.set_title('Bellek (MB)'); ax3.legend()
    plt.tight_layout()
    plt.show()