from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
from util import *
from collections import OrderedDict
import xml.etree.ElementTree

app = Flask(__name__, static_folder = "../dist/static",
            template_folder = "../dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

co2_xml = xml.etree.ElementTree.parse('data/co2.xml').getroot()
population_xml = xml.etree.ElementTree.parse('data/population.xml').getroot()

co2_dict = {}
population_dict = {}

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

@app.route("/api/co2/<year>/<percapita>/<top>")
def get_co2_top_list(year, percapita, top):
    this_year_co2 = {}
    for name, country_data in co2_dict.items():
        value = float(country_data[year])
        population = int(population_dict[name][year])
        if int(percapita) and population > 0:
            value = round(value * 1000 / population, 2)
        this_year_co2[name] = value
    top_list = sorted(this_year_co2.items(), key=lambda t: t[1], reverse=True)[:20]
    return jsonify(top_list)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")
