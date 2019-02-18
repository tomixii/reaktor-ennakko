from flask import Flask, render_template, jsonify, request, send_file
import xml.etree.ElementTree
app = Flask(__name__, template_folder="templates")

co2_xml = xml.etree.ElementTree.parse('data/co2.xml').getroot()
population_xml = xml.etree.ElementTree.parse('data/population.xml').getroot()

co2_dict = {}
population_dict = {}

for country_data in population_xml.iter('record'):
    key = ''
    value = 0
    for field in country_data.findall('field'):
        if field.attrib['name'] == 'Country or Area':
            key += field.text.lower() + '_'
            continue
        if field.attrib['name'] == 'Year':
            key += field.text
        if field.attrib['name'] == 'Value':
            if field.text is not None:
                value = int(field.text)
    population_dict[key] = value

for country_data in co2_xml.iter('record'):
    key = ''
    value = 0
    for field in country_data.findall('field'):
        if field.attrib['name'] == 'Country or Area':
            key += field.text.lower() + '_'
            continue
        if field.attrib['name'] == 'Year':
            key += field.text
        if field.attrib['name'] == 'Value':
            if field.text is not None:
                value = float(field.text)
    co2_dict[key] = value

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/co2/<country>/<year>")
def get_co2(country, year):
    data_value = co2_dict.get(country + '_' + year)
    if data_value is not None and data_value > 0:
        return str(data_value) + 'kt'
    else:
        return "-1"

@app.route("/api/population/<country>/<year>")
def get_population(country, year):
    data_value = population_dict.get(country + '_' + year)
    if data_value is not None and data_value > 0:
        return str(data_value)
    else:
        return "-1"
