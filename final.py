from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


def create_graph(nodes, ways):
    G = nx.Graph()

    for node_id, coords in nodes.items():
        G.add_node(node_id, pos=coords)

    for way_id, way_nodes in ways.items():
        for i in range(len(way_nodes) - 1):
            G.add_edge(way_nodes[i], way_nodes[i + 1])

    return G

def visualize_graph(graph):
    pos = nx.get_node_attributes(graph, "pos")
    nx.draw(graph, pos, with_labels=False, node_size=1, font_size=1)
    plt.show()

def visualize_graph2(graph, figure_size=(45, 45), dpi=900):
    pos = nx.get_node_attributes(graph, "pos")
    plt.figure(figsize=figure_size)
    nx.draw(graph, pos, with_labels=False, node_size=1, font_size=5)

    plt.show()

def visualize_graph3(graph, path ,figure_size=(60, 60), dpi=900):
    pos = nx.get_node_attributes(graph, "pos")
    plt.figure(figsize=figure_size)
    nx.draw(graph, pos, with_labels=False, font_color='black', node_size=100, node_color='lightgray')
    # Draw the A* path on top of the graphmodule
    nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color='red', node_size=500)
    nx.draw_networkx_edges(graph, pos, edgelist=list(zip(path, path[1:])), edge_color='red', width=2)
    plt.show()





def main():
    xml_file = "dataSmall.xml.xml"  # Replace with the path to your OSM XML file
    nodes, ways = parse_osm_xml(xml_file)
    osm_graph = create_graph(nodes, ways)
    # print(osm_graph.nodes)
    path = nx.astar_path(osm_graph, '937967081', '5865558098')
    visualize_graph3(osm_graph, path)

    # adjacency_list = {}
    # for node in osm_graph.nodes:
    #     neighbors = list(osm_graph.neighbors(node))
    #     adjacency_list[node] = [(neighbor, 1) for neighbor in neighbors]
    # print(adjacency_list['11117672234'])
    # graph1 = Graph(adjacency_list)
    # path = graph1.a_star_algorithm('2467954536', '837555444')

        # Assuming 'A' and 'D' are nodes in the OSM graphmodule
        # osm_subgraph = nx.subgraph(osm_graph, path)
        # print(path)
        # visualize_graph2(osm_subgraph)

if __name__ == "__main__":
    main()
