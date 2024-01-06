from flask import Flask, render_template
import subprocess
from src.graphmodule import GraphClass as Graph
from src.XmlModule.xmlclass import XmlClass as Xml

app = Flask(__name__)
xml_file = "./data/raw/dataWaypoints.xml"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/runcode/<int:example_number>')
def run_code(example_number):
    nodes, ways, waypoints, labels = Xml.parse_osm_xml(xml_file)
    osm_graph = Graph(nodes, ways, waypoints, labels)
    if example_number == 0:
        path = osm_graph.a_star_algorithm('937967081', '460927821')
        osm_graph.visualize_path(path)
    elif example_number == 1:
        path = osm_graph.a_star_algorithm('384328567', '1778569991')
        osm_graph.visualize_path(path)
    elif example_number == 2:
        path = osm_graph.a_star_algorithm('2120847437', '3741575976')
        osm_graph.visualize_path(path)

    return '300'


if __name__ == '__main__':
    app.run(debug=True)
