from src.graphmodule import GraphClass as Graph
from src.XmlModule.xmlclass import XmlClass as Xml


def main():
    xml_file = "./data/raw/data.xml"  # Replace with the path to your OSM XML file
    nodes, ways = Xml.parse_osm_xml(xml_file)
    osm_graph = Graph(nodes, ways)
    path = osm_graph.a_star_algorithm('937967081', '5865558098')

    # osm_graph.visualize()
    osm_graph.visualize_path(path)


if __name__ == "__main__":
    main()
