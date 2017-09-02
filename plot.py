import matplotlib.pyplot as plt
import numpy as np
import pickle

with open('track_location_count.p', 'rb') as f:
    edge_frequency = pickle.load(f)

edges_to_plot = [item[0] for item in edge_frequency if item[1] >= 2500]
save_path = 'images/frequent_edges_(>25%).png'

with open('game-board.p', 'rb') as f:
    board = pickle.load(f)

def draw_edge(edge, dots, color):
    x0 = edge[0][0]
    y0 = edge[0][1]
    x1 = edge[1][0]
    y1 = edge[1][1]
    plt.scatter(x=np.linspace(x0 + y0 * 0.5, x1 + y1 * 0.5, dots), y=np.linspace(y0 * 0.866, y1 * 0.866, dots),
                s=0.6, c=color)


plt.figure(figsize=(7.44, 4.3))
dots = 7
for edge in board.edges():
    if board[edge[0]][edge[1]]['weight'] == 2:
        draw_edge(edge, dots - 3, 'y')
edges = edges_to_plot
for edge in edges:
    draw_edge(edge, dots, 'r')
nodes = board.nodes()
plt.scatter(x=[n[0] + n[1] * 0.5 for n in nodes], y=[n[1] * 0.866 for n in nodes], s=3)
plt.axis('off')
if save_path is not None:
    plt.savefig(save_path)
plt.close()
