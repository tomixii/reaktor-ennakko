from flask import Flask, render_template, jsonify, request, send_file
import xml.etree.ElementTree
co2 = xml.etree.ElementTree.parse('data/co2.xml').getroot()
population = xml.etree.ElementTree.parse('data/population.xml').getroot()

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/co2/<country>/<year>")
def get_co2():

    return "0"

@app.route("/api/population/<country>/<year>")
def get_population():
    return "0"
