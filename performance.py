import matplotlib.pyplot as plt
import os, psutil, time
from game_logic import TicTacToe
from ai_engine import GameAI

def get_memory_usage():
    try: return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
    except: return 0

def run_analysis_graph(grid_size=3, max_depth=4):
    depths = list(range(1, max_depth + 1))
    res = {'minimax': {'t': [], 'n': [], 'm': []}, 'alphabeta': {'t': [], 'n': [], 'm': []}}
    
    for d in depths:
        for method in ['minimax', 'alphabeta']:
            m_start = get_memory_usage()
            g = TicTacToe(grid_size); ai = GameAI(g)
            
            start = time.perf_counter()
            if method == 'minimax': 
                # ai_engine içindeki doğru fonksiyon ismiyle güncellendi
                ai.minimax_only_nodes(d, True)
            else: 
                ai.alpha_beta(d, float('-inf'), float('inf'), True, time.perf_counter(), 10.0)
            t = time.perf_counter() - start
            
            res[method]['t'].append(t)
            res[method]['n'].append(ai.nodes_visited)
            res[method]['m'].append(max(0.01, get_memory_usage() - m_start))

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle(f"{grid_size}x{grid_size} Tahta Analizi")
    ax1.plot(depths, res['minimax']['t'], 'r-o', label='MM'); ax1.plot(depths, res['alphabeta']['t'], 'b-s', label='AB')
    ax1.set_title('Sure (sn)'); ax1.legend()
    ax2.plot(depths, res['minimax']['n'], 'r-o', label='MM'); ax2.plot(depths, res['alphabeta']['n'], 'b-s', label='AB')
    ax2.set_yscale('log'); ax2.set_title('Dugum (Log)'); ax2.legend()
    ax3.plot(depths, res['minimax']['m'], 'r-o', label='MM'); ax3.plot(depths, res['alphabeta']['m'], 'b-s', label='AB')
    ax3.set_title('Bellek (MB)'); ax3.legend()
    plt.tight_layout()
    plt.show()