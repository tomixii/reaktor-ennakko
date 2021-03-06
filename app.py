from flask import Flask, render_template, jsonify, abort
from flask_cors import CORS
from util import *
from collections import OrderedDict
import xml.etree.ElementTree

app = Flask(__name__, static_folder = "dist/static",
            template_folder = "dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

co2_xml = xml.etree.ElementTree.parse('xml_data/co2.xml').getroot()
population_xml = xml.etree.ElementTree.parse('xml_data/population.xml').getroot()

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

@app.route("/")
def index():
    return render_template("index.html")

#-------SIMPLE API------
@app.route("/api/co2/<country>")
def get_co2(country):
    return jsonify(co2_dict.get(country))

@app.route("/api/population/<country>")
def get_population(country):
    return jsonify(population_dict.get(country))

@app.route("/api/co2/<country>/<year>")
def get_co2_with_year(country, year):
    return str(search_dict(co2_dict, country, year))

@app.route("/api/population/<country>/<year>")
def get_population_with_year(country, year):
    return str(search_dict(population_dict, country, year))

@app.route("/api/countries")
def get_countries():
    return jsonify(list(population_dict.keys()))


@app.route("/api/co2percapita/<year>")
def get_co2_top_list(year):
    this_year_co2 = {}
    for name, country_data in co2_dict.items():
        value = float(country_data[year])
        population = int(population_dict[name][year])
        if population > 0:
            value = round(value * 1000 / population, 2)
            if value > 100:
                value = 0
            this_year_co2[name.capitalize()] = value
    top_list = sorted(this_year_co2.items(), key=lambda t: t[1], reverse=True)[:20]
    return jsonify(top_list)

@app.route("/api/greatpowers/<year>")
def get_co2_great_powers(year):
    great_powers = ['united kingdom', 'china', 'france', 'germany', 'japan', 'russian federation', 'united states']
    world_co2 = co2_dict['world'][year]
    world_co2_percentage = 100
    this_year_co2 = {}
    for name in great_powers:
        value = (float(co2_dict[name][year]) / world_co2) * 100
        if value > 0:
            world_co2_percentage -= value
            this_year_co2[name.capitalize()] = round(value, 2)
    this_year_co2["Rest of the world"] = round(world_co2_percentage, 2)
    percentage_list = sorted(this_year_co2.items(), key=lambda t: t[1], reverse=True)
    return jsonify(percentage_list)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return abort(404)
