import networkx as nx
import pickle

board = nx.Graph()

# x has 20 values
# y has 13 values

x_dim = 20
y_dim = 13

for x in range(x_dim):
    for y in range(y_dim):
        board.add_node((x,y))

def exists(x, y):
    return x >=0 and x < x_dim and y >= 0 and y < y_dim

# create main grid
for node in board.nodes():
    neighbour = (node[0] - 1, node[1] + 1)
    if exists(*neighbour):
        board.add_edge(node, neighbour, weight=1)
    neighbour = (node[0] + 1, node[1])
    if exists(*neighbour):
        board.add_edge(node, neighbour, weight=1)
    neighbour = (node[0], node[1] + 1)
    if exists(*neighbour):
        board.add_edge(node, neighbour, weight=1)

# cut off sw corner
for node in board.nodes():
    if node[0] + node[1] < 8:
        board.remove_node(node)

# cut off nw corner
for node in board.nodes():
    if node[0] + node[1] > 27:
        board.remove_node(node)

# cut remaining ad-hoc
remove_nodes = [
    (8, 0),
    (7, 1),
    (1, 7),
    (0, 8),
    (9, 0),
    (0, 9),
    (10, 0),
    (10, 12),
    (11, 12),
    (12, 11),
    (12, 12),
    (13, 10),
    (13, 11),
    (13, 12),
    (14, 10),
    (14, 11),
    (14, 12),
    (15, 12),
    (18, 6),
    (18, 7),
    (18, 8),
    (18, 9),
    (19, 5),
    (19, 6),
    (19, 7),
    (19, 8)
]
board.remove_nodes_from(remove_nodes)
board_nodes_only = board.copy()
board_nodes_only.remove_edges_from(board.edges())

with open('board_nodes_only.p', 'wb') as f:
    pickle.dump(board_nodes_only, f)

# terrain
double_edges = [
    [(0, 10), (1, 10)],
    [(0, 11), (1, 10)],
    [(0, 11), (1, 11)],
    [(0, 12), (1, 11)],
    [(0, 12), (1, 12)],
    [(1, 8), (2, 8)],
    [(1, 9), (2, 8)],
    [(1, 9), (2, 9)],
    [(1, 9), (1, 10)],
    [(2, 7), (2, 8)],
    [(2, 11), (2, 12)],
    [(2, 7), (3, 6)],
    [(2, 7), (3, 7)],
    [(2, 11), (3, 11)],
    [(3, 5), (3, 6)],
    [(3, 7), (3, 8)],
    [(3, 10), (3, 11)],
    [(3, 5), (4, 5)],
    [(3, 6), (4, 6)],
    [(3, 7), (4, 6)],
    [(3, 7), (4, 7)],
    [(3, 10), (4, 10)],
    [(3, 11), (4, 11)],
    [(4, 10), (4, 11)],
    [(4, 11), (4, 12)],
    [(4, 4), (5, 4)],
    [(4, 10), (5, 10)],
    [(4, 12), (5, 11)],
    [(5, 7), (5, 8)],
    [(5, 9), (5, 10)],
    [(5, 11), (5, 12)],
    [(5, 3), (6, 3)],
    [(5, 4), (6, 4)],
    [(5, 5), (6, 4)],
    [(5, 5), (6, 5)],
    [(5, 6), (6, 5)],
    [(5, 6), (6, 6)],
    [(5, 7), (6, 6)],
    [(5, 9), (6, 9)],
    [(5, 12), (6, 11)],
    [(6, 3), (6, 4)],
    [(6, 6), (6, 7)],
    [(6, 11), (6, 12)],
    [(6, 2), (7, 2)],
    [(6, 3), (7, 2)],
    [(6, 3), (7, 3)],
    [(6, 4), (7, 4)],
    [(6, 7), (7, 7)],
    [(6, 11), (7, 11)],
    [(7, 3), (7, 4)],
    [(7, 6), (7, 7)],
    [(7, 10), (7, 11)],
    [(7, 3), (8, 3)],
    [(7, 5), (8, 5)],
    [(7, 6), (8, 5)],
    [(7, 6), (8, 6)],
    [(7, 10), (8, 10)],
    [(8, 2), (8, 3)],
    [(8, 9), (8, 10)],
    [(8, 3), (9, 2)],
    [(8, 9), (9, 9)],
    [(9, 8), (9, 9)],
    [(9, 8), (10, 8)],
    [(9, 11), (10, 11)],
    [(10, 7), (10, 8)],
    [(10, 10), (10, 11)],
    [(10, 7), (11, 7)],
    [(10, 10), (11, 10)],
    [(11, 6), (11, 7)],
    [(11, 9), (11, 10)],
    [(11, 7), (12, 6)],
    [(11, 8), (12, 8)],
    [(11, 9), (12, 8)],
    [(11, 9), (12, 9)],
    [(12, 6), (12, 7)],
    [(12, 7), (12, 8)],
    [(12, 7), (13, 6)],
    [(12, 7), (13, 7)],
    [(13, 6), (13, 7)],
    [(13, 6), (14, 6)],
    [(14, 5), (14, 6)],
    [(14, 2), (15, 2)],
    [(14, 3), (15, 2)],
    [(14, 3), (15, 3)],
    [(14, 4), (15, 3)],
    [(14, 4), (15, 4)],
    [(14, 5), (15, 4)],
    [(14, 5), (15, 5)],
    [(14, 6), (15, 5)],
    [(14, 6), (15, 6)],
    [(14, 7), (15, 6)],
    [(15, 1), (15, 2)],
    [(15, 6), (15, 7)],
    [(15, 0), (16, 0)],
    [(15, 1), (16, 0)],
    [(15, 1), (16, 1)],
    [(15, 7), (16, 6)],
    [(16, 3), (17, 3)],
    [(16, 4), (17, 3)],
    [(16, 4), (17, 4)],
    [(16, 5), (17, 4)],
    [(16, 5), (17, 5)],
    [(16, 6), (17, 5)],
    [(16, 6), (17, 6)],
    [(16, 7), (17, 6)],
    [(16, 7), (17, 7)],
    [(16, 8), (17, 7)],
    [(16, 8), (17, 8)],
    [(16, 9), (17, 8)]
]

for edge in double_edges:
    board[edge[0]][edge[1]]['weight'] = 2

with open('game-board.p', 'wb') as f:
    pickle.dump(board, f)

# cities
cities = [
    ('SEATTLE', (0, 12)),
    ('PORTLAND', (0, 11)),
    ('MEDFORD', (1, 9)),
    ('SACRAMENTO', (2, 7)),
    ('SAN FRANCISCO', (2, 6)),
    ('LOS ANGELES', (5, 3)),
    ('SAN DIEGO', (6, 2)),
    ('HELENA', (3, 11)),
    ('BISMARK', (7, 11)),
    ('DULUTH', (10, 11)),
    ('MINNEAPOLIS', (10, 10)),
    ('CHICAGO', (13, 9)),
    ('CINCINNATI', (15, 7)),
    ('BUFFALO', (15, 10)),
    ('SALT LAKE CITY', (4, 8)),
    ('DENVER', (7, 7)),
    ('OMAHA', (9, 7)),
    ('SANTA FE', (8, 4)),
    ('KANSAS CITY', (11, 6)),
    ('OKLAHOMA CITY', (11, 4)),
    ('ST. LOUIS', (13, 6)),
    ('PHOENIX', (7, 3)),
    ('EL PASO', (10, 1)),
    ('HOUSTON', (14, 0)),
    ('DALLAS', (13, 2)),
    ('MEMPHIS', (15, 3)),
    ('ATLANTA', (17, 2)),
    ('NEW ORLEANS', (16, 0)),
    ('BOSTON', (17, 10)),
    ('NEW YORK', (17, 8)),
    ('WASHINGTON', (17, 7)),
    ('RICHMOND', (18, 5)),
    ('WINSTON', (17, 4)),
    ('CHARELSTON', (19, 2)),
    ('JACKSONVILLE', (19, 0))
]


print(board.nodes())
print(board.edges())