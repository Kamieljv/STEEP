""" app.py

    Required packages:
    - flask
    - pandas
    - os


    Usage:

    Start the flask server by running:

        $ python app.py

    And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""

from flask import Flask, render_template, request, json
import geopandas as gpd

from src.vehicle_config import VehicleConfig
from src.emission_calculator import EmissionCalculator
from src.routing import Routing


# Load vehicle configuration class
v_config = VehicleConfig()
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Sets vehicle parameter options and renders home-page."""
    fuels = v_config.fuels
    segments = v_config.segments
    standards = v_config.standards
    return render_template('home.html', fuels=fuels, segments=segments, standards=standards, title="Home")


@app.route('/calculate_route', methods=['POST'])
def calculate_route():
    """Gets route configuration; calculates route; returns route to view as JSON."""
    # Calculate route
    # departure = request.form['departure']
    startLat, startLon = request.form['start-coords'].split(", ")
    destLat, destLon = request.form['dest-coords'].split(", ")
    router = Routing()
    route = router.get_route(float(startLat), float(startLon), float(destLat), float(destLon))

    # # Calculate emissions
    # fuel = request.form['fuel']
    # segment = request.form['segment']
    # standard = request.form['standard']
    # calculator = EmissionCalculator('data/Ps_STEEP_a_emis.csv', fuel=fuel, segment=segment, standard=standard)

    return route.to_json()

@app.route('/about', methods=['GET'])
def about():
    """Renders about-page."""
    return render_template('about.html', title="About")

@app.route('/help', methods=['GET'])
def help():
    """Renders help-page."""
    return render_template('help.html', title="Help")

@app.after_request
def add_header(response):
    """Add headers to both force latest IE rendering engine or Chrome Frame; disable cache."""
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['Pragma'] = 'no-cache'
    return response

if __name__ == '__main__':
    app.run(debug=True)