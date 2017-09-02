import networkx as nx
import copy


class Game:

    def __init__(self, player_list, board, board_track_only):
        self.player_list = player_list
        self.board = board
        self.board_track_only = board_track_only
        self.round_counter = 0

    def lay_track(self, edge_list):
        for edge in edge_list:
            self.board[edge[0]][edge[1]]['weight'] = 0
            self.board_track_only.add_edge(edge[0], edge[1])


    def get_remaining_distance(self, home_node, objective_nodes):
        # THE IDEA HERE: get the closest remaining objective, lay track to it, get the next closest, lay track to it,
        # etc. until all remaining objectives have been reached - count total distance covered. Remember which track
        # was added so we can revert afterwards (much faster than copying)
        remaining_distance = 0
        nodes = copy.copy(objective_nodes)
        added_track_weights = {}
        while len(nodes) > 0:
            nodes = [(x, nx.astar_path_length(self.board, home_node, x)) for x in nodes]
            nodes.sort(key=lambda x: x[1])
            for i, node in enumerate(nodes):
                if node[1] != 0:
                    break
                nodes = nodes[1:]
            if len(nodes) == 0:
                break
            remaining_distance += nodes[0][1]
            remaining_edges = self.get_nonzero_edges_shortest_path(self.board, home_node, nodes[0][0])
            nodes = nodes[1:]
            added_track_weights.update(self.set_weights_to_zero(remaining_edges))
            nodes = [x[0] for x in nodes]
        # revert back to intended board state
        for edge in added_track_weights:
            self.board[edge[0]][edge[1]]['weight'] = added_track_weights[edge]
        return remaining_distance

    def assess_objective_difficulty(self, objective_nodes):
        # find node with nearest neighbours (using distance estimates), select as home, then use get_remaining_distance
        return self.get_remaining_distance(self.find_central_node(objective_nodes), objective_nodes)

    def find_central_node(self, nodes):
        neighbour_dist = []
        for node1 in nodes:
            cum_dist = 0
            for node2 in nodes:
                if node1 is node2:
                    continue
                cum_dist += self.dist_est(node1, node2)
            neighbour_dist.append((node1, cum_dist))
        neighbour_dist.sort(key=lambda x: x[1])
        return neighbour_dist[0][0]

    @staticmethod
    def dist_est(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        if dx * dy < 0:
            return abs(dx) + abs(dy) - min(abs(dx), abs(dy))
        else:
            return abs(dx) + abs(dy)

    @staticmethod
    def nonzero_segments(graph, path):
        trimmed_path = []
        previous_vertex = path[0]
        for vertex in path[1:]:
            trimmed_path.append(previous_vertex)
            if graph[previous_vertex][vertex]['weight'] != 0:
                trimmed_path.append(vertex)
            else:
                trimmed_path.pop()
            previous_vertex = vertex
        return trimmed_path

    @staticmethod
    def nonzero_edges(graph, path):
        edge_list = []
        previous_vertex = path[0]
        for vertex in path[1:]:
            if graph[previous_vertex][vertex]['weight'] != 0:
                edge_list.append((previous_vertex, vertex))
            previous_vertex = vertex
        return edge_list

    def get_nonzero_edges_shortest_path(self, graph, home, target):
        return self.nonzero_edges(graph, nx.astar_path(graph, home, target))

    def set_weights_to_zero(self, edge_list):
        revert_dict = {}
        for edge in edge_list:
            revert_dict[edge] = self.board[edge[0]][edge[1]]['weight']
            self.board[edge[0]][edge[1]]['weight'] = 0
        return revert_dict

    def edge_weights(self, edge_list):
        return [self.board[edge[0]][edge[1]]['weight'] for edge in edge_list]
