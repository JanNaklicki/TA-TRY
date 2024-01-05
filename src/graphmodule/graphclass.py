# class GraphClass:
#     def __init__(self, adjacency_list):
#         self.adjacency_list = adjacency_list
#
#     def get_neighbors(self, v):
#         return self.adjacency_list[v]
#
#     def h(self, n):
#         H = {
#             'A': 1,
#             'B': 1,
#             'C': 2,
#             'D': 1,
#             'E': 1,
#         }
#
#         return 1
#         # return H[n]
#
#     def a_star_algorithm(self, start_node, stop_node):
#         open_list = set([start_node])
#         closed_list = set([])
#
#         g = {}
#         g[start_node] = 0
#
#         parents = {}
#         parents[start_node] = start_node
#
#         while len(open_list) > 0:
#             n = None
#
#             for v in open_list:
#                 if n is None or g[v] + self.h(v) < g[n] + self.h(n):
#                     n = v
#
#             if n is None:
#                 print('Path does not exist!')
#                 return None
#
#             if n == stop_node:
#                 reconst_path = []
#
#                 while parents[n] != n:
#                     reconst_path.append(n)
#                     n = parents[n]
#
#                 reconst_path.append(start_node)
#                 reconst_path.reverse()
#
#                 print('Path found: {}'.format(reconst_path))
#                 return reconst_path
#
#             for (m, weight) in self.get_neighbors(n):
#                 if m not in open_list and m not in closed_list:
#                     open_list.add(m)
#                     parents[m] = n
#                     g[m] = g[n] + weight
#                 else:
#                     if g[m] > g[n] + weight:
#                         g[m] = g[n] + weight
#                         parents[m] = n
#
#                         if m in closed_list:
#                             closed_list.remove(m)
#                             open_list.add(m)
#
#             open_list.remove(n)
#             closed_list.add(n)
#
#         print('Path does not exist!')
#         return None
import matplotlib.pyplot as plt


import networkx as nx


class GraphClass:
    __figure_size = (60,60)
    __base_node_size = 50
    __base_node_color = 'lightgray'
    __base_edge_color = 'black'

    __path_node_color = 'red'
    __path_node_size = 500
    def __init__(self, nodes, ways):
        # prepare graph
        self.graph = nx.Graph()
        # self.graph.add_weighted_edges_from(adjacency_list)
        for node_id, coords in nodes.items():
            self.graph.add_node(node_id, pos=coords)
        for way_id, way_nodes in ways.items():
            for i in range(len(way_nodes) - 1):
                self.graph.add_edge(way_nodes[i], way_nodes[i + 1], weight=5) #TODO: change it so it will get time here

    def h(self, n):
        H = {
            'A': 1,
            'B': 30,
            'C': 10,
            'D': 1,
            'E': 1,
        }

        return 1

    def get_neighbors(self, v):
        return list(self.graph.edges(v, data=True))


    def a_star_algorithm(self, start_node, stop_node):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        open_list = set([start_node])
        closed_list = set([])

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}

        g[start_node] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start_node] = start_node

        while len(open_list) > 0:
            n = None

            # find a node with the lowest value of f() - evaluation function
            for v in open_list:
                if n == None or g[v] + self.h(v) < g[n] + self.h(n):
                    n = v

            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == stop_node:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start_node)

                reconst_path.reverse()

                print('Path found: {}'.format(reconst_path))
                return reconst_path

            # for all neighbors of the current node do
            for data in self.get_neighbors(n):
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                neighbour = data[1]
                weight = data[2]['weight']
                if neighbour not in open_list and neighbour not in closed_list:
                    open_list.add(neighbour)
                    parents[neighbour] = n
                    g[neighbour] = g[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[neighbour] > g[n] + weight:
                        g[neighbour] = g[n] + weight
                        parents[neighbour] = n

                        if neighbour in closed_list:
                            closed_list.remove(neighbour)
                            open_list.add(neighbour)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    def a_star_algorithm_package(self, start_node, stop_node):
        if start_node not in self.graph.nodes or stop_node not in self.graph.nodes:
            print('Start or stop node not in the graph!')
            return None

        path = nx.astar_path(self.graph, start_node, stop_node, heuristic=lambda n, goal: self.h(n, goal),
                             weight='weight')

        if not path:
            print('Path does not exist!')
            return None

        print('Path found: {}'.format(path))
        return path

    def visualize(self):
        plt.figure(figsize=self.__figure_size)

        pos = nx.get_node_attributes(self.graph, "pos")
        # Draw base graph
        nx.draw(self.graph, pos, with_labels=False, node_size=self.__base_node_size, node_color=self.__base_node_color)
        plt.show()

    def visualize_path(self, path):
        plt.figure(figsize=self.__figure_size)

        pos = nx.get_node_attributes(self.graph, "pos")
        # Draw base graph
        nx.draw(self.graph, pos, with_labels=False, node_size=self.__base_node_size, node_color=self.__base_node_color)
        # Draw the A* path on top of the graph
        nx.draw_networkx_nodes(self.graph, pos, nodelist=path, node_color=self.__path_node_color, node_size=self.__base_node_size)
        nx.draw_networkx_edges(self.graph, pos, edgelist=list(zip(path, path[1:])), edge_color=self.__base_edge_color, width=2)
        plt.show()

# Example usage
# adjacency_list = [('A', 'B', 1), ('A', 'C', 2), ('B', 'C', 2), ('B', 'D', 1), ('D', 'E', 1), ('E','C',1)]
# graph = GraphClass(adjacency_list)
# path = graph.a_star_algorithm('A', 'E')





from collections import deque

# class Graph:
#     # example of adjacency list (or rather map)
#     # adjacency_list = {
#     # 'A': [('B', 1), ('C', 3), ('D', 7)],
#     # 'B': [('D', 5)],
#     # 'C': [('D', 12)]
#     # }
#
#     def __init__(self, adjacency_list):
#         self.adjacency_list = adjacency_list
#
#     def get_neighbors(self, v):
#         return self.adjacency_list[v]
#
#     # heuristic function with equal values for all nodes
#     def h(self, n):
#         H = {
#             'A': 1,
#             'B': 1,
#             'C': 2,
#             'D': 1,
#             'E': 1,
#         }
#
#         return H[n]
#
    # def a_star_algorithm(self, start_node, stop_node):
    #     # open_list is a list of nodes which have been visited, but who's neighbors
    #     # haven't all been inspected, starts off with the start node
    #     # closed_list is a list of nodes which have been visited
    #     # and who's neighbors have been inspected
    #     open_list = set([start_node])
    #     closed_list = set([])
    #
    #     # g contains current distances from start_node to all other nodes
    #     # the default value (if it's not found in the map) is +infinity
    #     g = {}
    #
    #     g[start_node] = 0
    #
    #     # parents contains an adjacency map of all nodes
    #     parents = {}
    #     parents[start_node] = start_node
    #
    #     while len(open_list) > 0:
    #         n = None
    #
    #         # find a node with the lowest value of f() - evaluation function
    #         for v in open_list:
    #             if n == None or g[v] + self.h(v) < g[n] + self.h(n):
    #                 n = v;
    #
    #         if n == None:
    #             print('Path does not exist!')
    #             return None
    #
    #         # if the current node is the stop_node
    #         # then we begin reconstructin the path from it to the start_node
    #         if n == stop_node:
    #             reconst_path = []
    #
    #             while parents[n] != n:
    #                 reconst_path.append(n)
    #                 n = parents[n]
    #
    #             reconst_path.append(start_node)
    #
    #             reconst_path.reverse()
    #
    #             print('Path found: {}'.format(reconst_path))
    #             return reconst_path
    #
    #         # for all neighbors of the current node do
    #         for (m, weight) in self.get_neighbors(n):
    #             # if the current node isn't in both open_list and closed_list
    #             # add it to open_list and note n as it's parent
    #             if m not in open_list and m not in closed_list:
    #                 open_list.add(m)
    #                 parents[m] = n
    #                 g[m] = g[n] + weight
    #
    #             # otherwise, check if it's quicker to first visit n, then m
    #             # and if it is, update parent data and g data
    #             # and if the node was in the closed_list, move it to open_list
    #             else:
    #                 if g[m] > g[n] + weight:
    #                     g[m] = g[n] + weight
    #                     parents[m] = n
    #
    #                     if m in closed_list:
    #                         closed_list.remove(m)
    #                         open_list.add(m)
    #
    #         # remove n from the open_list, and add it to closed_list
    #         # because all of his neighbors were inspected
    #         open_list.remove(n)
    #         closed_list.add(n)
    #
    #     print('Path does not exist!')
    #     return None
#
#
#