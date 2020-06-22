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
from datetime import datetime, timedelta

from src.emission_calculator import EmissionCalculator
from src.routing import Routing

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Sets vehicle parameter options and renders home-page."""
    calculator = EmissionCalculator()
    options = calculator.get_options({'fuel':"", 'segment':"", 'standard': ""})
    return render_template('home.html',
                           fuels=options['fuel'],
                           segments=options['segment'],
                           standards=options['standard'],
                           routetypes=['Eco', 'Fastest'],
                           title="Home")

@app.route('/getoptions', methods=['POST', 'GET'])
def getoptions():
    """Updates vehicle parameter options based on user's choice."""
    calculator = EmissionCalculator()
    options = calculator.get_options({'fuel':request.form['fuel'], 'segment':request.form['segment'], 'standard':""})
    return jsonify(options)

@app.route('/calculate_route', methods=['POST'])
def calculate_route():
    """Gets route configuration; calculates route; returns route to view as JSON."""
    # Check if time is not in past, otherwise change to present
    departure = datetime.strptime(request.form['departure'], '%Y-%m-%d %H:%M')
    if departure < datetime.now():
        departure = datetime.now() + timedelta(minutes=1)

    # Adding 4 more departure times
    departures = [datetime.strftime(departure, '%Y-%m-%d %H:%M')]
    for i in range(4):
        departure += timedelta(minutes=5)
        departures.append(datetime.strftime(departure, '%Y-%m-%d %H:%M'))

    dep_fmt = []
    for dep in departures:
        # Define and format the departure time variable
        tz = pytz.timezone('Europe/Amsterdam') # set time zone
        fmt = '%Y-%m-%dT%H:%M:%S%z' # set date format
        t = [int(x) for x in re.split(' |-|:', dep)] # convert to integers
        departure = tz.localize(datetime(t[0], t[1], t[2], t[3], t[4], 0)).strftime(fmt)
        departure = departure[:-2] + ':' + departure[-2:]
        dep_fmt.append(departure)

    routes = {}
    for i, depa in enumerate(dep_fmt):
        # Calculate route
        startLat, startLon = request.form['start-coords'].split(", ")
        destLat, destLon = request.form['dest-coords'].split(", ")
        traffic = 'traffic' in request.form
        router = Routing()
        route = router.get_route(float(startLat), float(startLon), float(destLat), float(destLon), depa, request.form["route-type"], traffic)

        # Calculate emissions
        fuel = request.form['fuel']
        segment = request.form['segment']
        standard = request.form['standard']
        calculator = EmissionCalculator(fuel=fuel, segment=segment, standard=standard)
        emfac_route = calculator.calculate_ec_factor(route)
        emissions, distance, time = calculator.calculate_stats()

        routes['route'+ str(i)] = {'route': emfac_route.to_json(), 'emissions': emissions,
                             'distance': distance, 'time': time, 'departure': depa }

    return routes

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