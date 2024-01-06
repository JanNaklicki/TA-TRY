import xml.etree.ElementTree as ET


class XmlClass:
    @staticmethod
    def parse_osm_xml(xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        nodes = {}
        ways = {}
        waypoints = {}
        labels = {}

        for element in root.findall(".//node"):
            node_id = element.attrib["id"]
            lat = float(element.attrib["lat"])
            lon = float(element.attrib["lon"])

            # Check if the "natural" tag exists
            natural_tag = element.find(".//tag[@k='natural']")
            natural_value = natural_tag.attrib["v"] if natural_tag is not None else None

            information_tag = element.find(".//tag[@k='information']")
            information_value = information_tag.attrib["v"] if information_tag is not None else None

            # Check if the node is a peak and add it to waypoints

            if information_value == "guidepost" or natural_value == "peak":
                name_tag = element.find(".//tag[@k='name:pl']")
                name_value = name_tag.attrib["v"] if name_tag is not None else ''
                if name_value == '':
                    # If "name:pl" tag is not found for peaks, use "name" tag for guideposts
                    name_tag = element.find(".//tag[@k='name']")
                    name_value = name_tag.attrib["v"] if name_tag is not None else ''
                labels[node_id] = name_value + '\n' + node_id
                waypoints[node_id] = (lon, lat)
                continue
            nodes[node_id] = (lon, lat)

        for element in root.findall(".//way"):
            way_id = element.attrib["id"]
            way_nodes = [nd.attrib["ref"] for nd in element.findall(".//nd")]
            ways[way_id] = way_nodes

        return nodes, ways, waypoints, labels
