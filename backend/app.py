from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import xml.etree.ElementTree

app = Flask(__name__, static_folder = "../dist/static",
            template_folder = "../dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

co2_xml = xml.etree.ElementTree.parse('data/co2.xml').getroot()
population_xml = xml.etree.ElementTree.parse('data/population.xml').getroot()

co2_dict = {}
population_dict = {}

#-------UTIL FUNCTIONS---------
def parse_country(country_data):
    name = ''
    year = ''
    value = 0
    for field in country_data.findall('field'):
        if field.attrib['name'] == 'Country or Area':
            name = field.text.lower()
        elif field.attrib['name'] == 'Year':
            year = field.text
        elif field.attrib['name'] == 'Value' and field.text is not None:
            value = field.text
    return name, year, value

def create_response(country_data, country, year):
    if country_data is not None:
        data_value = country_data.get(year)
        if data_value is not None and data_value > 0:
            response = {
                'country': country,
                'year': year,
                'value': str(data_value)
            }
            return jsonify(response)
    return jsonify({'value': '-1'})


#------CREATE DICTIONARIES FROM XMLS------
for country_data in population_xml.iter('record'):
    name, year, value = parse_country(country_data)
    if population_dict.get(name) is None:
        population_dict[name] = {}
    population_dict[name][year] = int(value)

for country_data in co2_xml.iter('record'):
    name, year, value = parse_country(country_data)
    if co2_dict.get(name) is None:
        co2_dict[name] = {}
    co2_dict[name][year] = float(value)

#-------SIMPLE API------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/co2/<country>/<year>")
def get_co2(country, year):
    return create_response(co2_dict.get(country), country, year)

@app.route("/api/population/<country>/<year>")
def get_population(country, year):
    return create_response(population_dict.get(country), country, year)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")
