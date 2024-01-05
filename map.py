# import xml.etree.ElementTree as ET
#
# def is_valid_description(description):
#     # Check if the description contains only valid characters
#     valid_chars = set("0123456789/: h")
#     return all(char in valid_chars for char in description)
#
# def extract_trailing_way_information(xml_file):
#     # Parse the XML file
#     tree = ET.parse(xml_file)
#     root = tree.getroot()
#
#     trailing_way_information = []
#
#     # Iterate through all relation elements in the XML
#     for relation_element in root.findall(".//relation"):
#         # print(relation_element.find(".//tag[@k='route']").get('v') if relation_element.find(".//tag[@k='name']") is not None else '')
#         # Find all member elements in the relation that are of type 'way'
#         way_members = relation_element.findall(".//member[@type='way']")
#
#         # Extract information from each way member
#         for way_member in way_members:
#             way_id = way_member.get("ref")
#             way_element = root.find(f".//way[@id='{way_id}']")
#             way_coordinates = extract_coordinates_from_way(way_element, root)
#
#             # Extract information from the relation
#             description = relation_element.find(".//tag[@k='description']")
#             distance = relation_element.find(".//tag[@k='distance']")
#             name = relation_element.find(".//tag[@k='name']")
#
#             # Check if the description contains only valid characters
#             if description is not None and is_valid_description(description.get('v')):
#             # Append the information to the array
#                 trailing_way_information.append({
#                     'description': description.get('v') if description is not None else '',
#                     'distance': distance.get('v') if distance is not None else '',
#                     'name': name.get('v') if name is not None else '',
#                     'way_coordinates': way_coordinates,
#                 })
#
#     return trailing_way_information
#
# def extract_coordinates_from_way(way_element, root):
#     # Extract coordinates from a way
#     node_elements = way_element.findall(".//nd")
#     coordinates = []
#
#     for node_element in node_elements:
#         node_id = node_element.get("ref")
#         node = root.find(f".//node[@id='{node_id}']")
#         lat = float(node.get("lat"))
#         lon = float(node.get("lon"))
#         coordinates.append((lat, lon))
#
#     return coordinates
#
# # Example usage
# xml_file_path = "data/raw/dataSmall.xml"
# trailing_way_information = extract_trailing_way_information(xml_file_path)
#
# # Display the result
# for index, way_info in enumerate(trailing_way_information, start=1):
#     print(f"Name: {way_info['name']} Description: {way_info['description']}, Coordinates: {way_info['way_coordinates']}") #Distance: {way_info['distance']}, Coordinates: {way_info['way_coordinates']}
#     # print()



import xml.etree.ElementTree as ET

def is_valid_description(description):
    # Check if the description contains only valid characters
    valid_chars = set("0123456789/: h")
    return all(char in valid_chars for char in description)

def extract_start_end_information(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    start_end_information = {}

    # Iterate through all relation elements in the XML
    test = root.findall(".//relation")
    for relation_element in root.findall(".//relation"):
        # Find all member elements in the relation that are of type 'way'
        way_members = relation_element.findall(".//member[@type='way']")

        # Extract information from each way member
        for way_member in way_members:
            way_id = way_member.get("ref")
            way_element = root.find(f".//way[@id='{way_id}']")
            way_coordinates = extract_coordinates_from_way(way_element, root)

            # Extract information from the relation
            description = relation_element.find(".//tag[@k='description']")
            name = relation_element.find(".//tag[@k='name']")

            # Check if the description contains only valid characters
            if description is not None and is_valid_description(description.get('v')):
                # Extract the start and end coordinates
                start_coordinates = way_coordinates[0]
                end_coordinates = way_coordinates[-1]

                # Create a unique key for the way based on start and end coordinates
                name_parts = name.get('v').split(' - ')
                start_name = name_parts[0] if len(name_parts) > 0 else ''
                end_name = name_parts[1] if len(name_parts) > 1 else ''

                # Create a unique key for the way based on start and end coordinates
                way_key = f"{start_coordinates}_{end_coordinates}"

                # Add the information to the dictionary
                start_end_information[way_key] = {
                    'start': {'coordinates': start_coordinates, 'name': start_name},
                    'end': {'coordinates': end_coordinates, 'name': end_name},
                }

    return start_end_information

def extract_coordinates_from_way(way_element, root):
    # Extract coordinates from a way
    node_elements = way_element.findall(".//nd")
    coordinates = []

    for node_element in node_elements:
        node_id = node_element.get("ref")
        node = root.find(f".//node[@id='{node_id}']")
        lat = float(node.get("lat"))
        lon = float(node.get("lon"))
        coordinates.append((lat, lon))

    return coordinates

# Example usage
xml_file_path = "data/raw/dataSmall.xml"
start_end_information = extract_start_end_information(xml_file_path)

# Display the result
for way_key, way_info in start_end_information.items():
    print(f"Way ID: {way_key}")
    print(f"Start: {way_info['start']}")
    print(f"End: {way_info['end']}")
    print()
