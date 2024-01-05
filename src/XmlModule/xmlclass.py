import xml.etree.ElementTree as ET


class XmlClass:
    @staticmethod
    def parse_osm_xml(xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        nodes = {}
        ways = {}

        for element in root.findall(".//node"):
            node_id = element.attrib["id"]
            lat = float(element.attrib["lat"])
            lon = float(element.attrib["lon"])
            nodes[node_id] = (lon, lat)

        for element in root.findall(".//way"):
            way_id = element.attrib["id"]
            way_nodes = [nd.attrib["ref"] for nd in element.findall(".//nd")]
            ways[way_id] = way_nodes

        return nodes, ways
