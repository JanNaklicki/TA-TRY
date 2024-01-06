import matplotlib.pyplot as plt


import networkx as nx


class GraphClass:
    __figure_size = (70, 70)

    __base_node_size = 1
    __base_node_color = 'none'
    __base_edge_color = 'black'

    __way_width = 1

    __path_node_color = 'none'
    __path_node_size = 2

    __peaks_node_color = '#AECF9C'
    __peaks_node_size = 900

    __label_font_size = 6

    def __init__(self, nodes, ways, waypoints, labels):
        # prepare graph
        self.graph = nx.Graph()
        self.labels = labels
        # self.graph.add_weighted_edges_from(adjacency_list)

        for node_id, coords in nodes.items():
            self.graph.add_node(node_id, pos=coords)
        for way_id, way_nodes in ways.items():
            for i in range(len(way_nodes) - 1):
                self.graph.add_edge(way_nodes[i], way_nodes[i + 1], weight=5)
        for waypoint_id, waypoint_coords in waypoints.items():
            self.graph.add_node(waypoint_id, pos=waypoint_coords)
            self.graph.nodes[waypoint_id]['type'] = 'waypoint'

    @staticmethod
    def h(n):
        return 1

    def get_neighbors(self, v):
        return list(self.graph.edges(v, data=True))


    def a_star_algorithm(self, start_node, stop_node):
        open_list = {start_node}
        closed_list = set([])
        g = {start_node: 0}
        parents = {start_node: start_node}

        while len(open_list) > 0:
            n = None

            # find a node with the lowest value of f() - evaluation function
            for v in open_list:
                if n is None or g[v] + self.h(v) < g[n] + self.h(n):
                    n = v

            if n is None:
                print('Path does not exist!')
                return None

            if n == stop_node:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start_node)

                reconst_path.reverse()

                print('Path found: {}'.format(reconst_path))
                return reconst_path

            for data in self.get_neighbors(n):
                neighbour = data[1]
                weight = data[2]['weight']
                if neighbour not in open_list and neighbour not in closed_list:
                    open_list.add(neighbour)
                    parents[neighbour] = n
                    g[neighbour] = g[n] + weight

                else:
                    if g[neighbour] > g[n] + weight:
                        g[neighbour] = g[n] + weight
                        parents[neighbour] = n

                        if neighbour in closed_list:
                            closed_list.remove(neighbour)
                            open_list.add(neighbour)

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

        img = plt.imread('./data/processed/map4.png')
        plt.imshow(img, extent=(min(pos.values())[0], max(pos.values())[0], min(pos.values())[1], max(pos.values())[1]))

        # base graph
        nx.draw(self.graph, pos, with_labels=False, node_size=self.__base_node_size, node_color=self.__base_node_color)

        # waypoints
        waypoint_nodes = [node for node, data in self.graph.nodes(data=True) if 'type' in data and data['type'] == 'waypoint']
        nx.draw_networkx_nodes(self.graph, pos, nodelist=waypoint_nodes, node_size=self.__peaks_node_size, node_color=self.__peaks_node_color)
        # labels
        labels = {node: self.labels[node] for node in waypoint_nodes}
        labelsOnGraph = nx.draw_networkx_labels(self.graph, pos, labels=labels, font_size=self.__label_font_size)
        for _, t in labelsOnGraph.items():
            t.set_rotation(45)

        plt.xlim(19.822898, 20.091935, )
        plt.ylim(49.178465, 49.276765)
        plt.savefig('./static/map.svg', format='svg', bbox_inches='tight')
        plt.close()

    def visualize_path(self, path):
        plt.figure(figsize=self.__figure_size)

        pos = nx.get_node_attributes(self.graph, "pos")

        img = plt.imread('./data/processed/map4.png')
        plt.imshow(img, extent=(19.822898, 20.091935, 49.178465, 49.276765))

        # base graph
        nx.draw(self.graph, pos, with_labels=False, node_size=self.__base_node_size, node_color=self.__base_node_color)

        # path on top of the graph
        nx.draw_networkx_nodes(self.graph, pos, nodelist=path, node_color=self.__path_node_color, node_size=self.__path_node_size)
        nx.draw_networkx_edges(self.graph, pos, edgelist=list(zip(path, path[1:])), edge_color='#FF521B', width=2)

        # waypoints
        waypoint_nodes = [node for node, data in self.graph.nodes(data=True) if 'type' in data and data['type'] == 'waypoint']
        nx.draw_networkx_nodes(self.graph, pos, nodelist=waypoint_nodes, node_size=500, node_color=self.__peaks_node_color)

        # labels
        labels = {node: self.labels[node] for node in waypoint_nodes}
        labelsOnGraph = nx.draw_networkx_labels(self.graph, pos, labels=labels, font_size=self.__label_font_size)
        for _, t in labelsOnGraph.items():
            t.set_rotation(45)

        plt.xlim(19.822898, 20.091935,)
        plt.ylim(49.178465, 49.276765)
        plt.savefig('./static/map.svg', format='svg', bbox_inches='tight')
        plt.close()
