""" app.py

    Required packages:
    - flask
    - pandas
    - os
    - pytz
    - re


    Usage:

    Start the flask server by running:

        $ python app.py

    And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""

from flask import Flask, render_template, request, jsonify
import pytz, re
from datetime import datetime

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

    # Define and format the departure time variable
    tz = pytz.timezone('Europe/Amsterdam') # set time zone
    fmt = '%Y-%m-%dT%H:%M:%S%z' # set
    t = [int(x) for x in re.split(' |-|:', request.form['departure'])] # convert to integers
    departure = tz.localize(datetime(t[0], t[1], t[2], t[3], t[4], 0)).strftime(fmt)
    departure = departure[:-2] + ':' + departure[-2:]

    # Calculate route
    startLat, startLon = request.form['start-coords'].split(", ")
    destLat, destLon = request.form['dest-coords'].split(", ")
    router = Routing()
    route = router.get_route(float(startLat), float(startLon), float(destLat), float(destLon), departure)

    # Calculate emissions
    fuel = request.form['fuel']
    segment = request.form['segment']
    standard = request.form['standard']
    calculator = EmissionCalculator('data/Ps_STEEP_a_emis.csv', fuel=fuel, segment=segment, standard=standard)
    emfac_route = calculator.calculate_emission_factor(route)
    emissions, distance, time = calculator.calculate_stats()

    return jsonify({'route': emfac_route.to_json(), 'emissions': emissions, 'distance': distance, 'time': time, 'departure': request.form['departure'] })

@app.route('/time_window', methods=['POST'])
def time_window():
    """Gets departure time; calculates time window (5 options with a 5 minute interval)"""

    # Get departure time
    router = Routing()
    departure = router.find('departure', router)

    # Calculate time window


    return None

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