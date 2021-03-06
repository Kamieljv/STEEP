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
from src.scenario_builder import Scenario

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

    tz = pytz.timezone('Europe/Amsterdam')

    # Check if time is not in past, otherwise change to present
    departure = datetime.strptime(request.form['departure'], '%Y-%m-%d %H:%M')
    departure = tz.localize(departure) # attach time zone
    if departure < datetime.now(tz):
        departure = datetime.now(tz) + timedelta(minutes=1)

    # Initialize routing object and build timewindow if required
    router = Routing()
    fmt = '%Y-%m-%dT%H:%M:%S%z'
    dep_fmt, future_tw = router.timewindow(departure, timestep=int(request.form['timestep']), outFormat=fmt) if 'timewindow' in request.form else ([datetime.strftime(departure, fmt)], True)
    default_route_idx = 0 if (future_tw) else 2 # specify the default route, which is 0 if the full timewindow (tw) is in the future

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
        default_route = 'true' if i == default_route_idx else 'false'
        routes['route' + str(i)] = {'route': emfac_route.to_json(), 'emissions': emissions,
                                    'distance': distance, 'time': time, 'departure': depa, 'default': default_route }

    if len(routes) > 1: # return all routes
        return routes
    else: # return a single route
        return routes['route0']

@app.route('/scenario', methods=['GET'])
def scenario():
    """Renders scenario-making page."""
    calculator = EmissionCalculator()
    options = calculator.get_options({'fuel':"", 'segment':"", 'standard': ""})
    return render_template('scenario.html',
                           title="Scenario Builder",
                           fuels=options['fuel'],
                           segments=options['segment'],
                           standards=options['standard'],
                           routetypes=['Eco', 'Fastest'])

@app.route('/calculate_scenario', methods=['POST'])
def calculate_scenario():
    data = request.form.to_dict()

    scenario = Scenario(**data)
    error = scenario.run()
    if error:
        return jsonify(error)

    tseries = scenario.timeseries()
    minDate, maxDate = datetime.strftime(tseries.index[0], "%Y-%m-%d"), datetime.strftime(tseries.index[-1], "%Y-%m-%d")
    tseries_lst = tseries.to_numpy()
    df_res = scenario.df_results
    df_res.index = df_res.index.strftime('%Y-%m-%dT%H:%M:%S%z')
    max = df_res[df_res['emissions'] == df_res['emissions'].max()] # max-emissions trip
    mean = df_res.mean() # average trip statistics

    return jsonify({'emissions': df_res.emissions.sum(), 'distance': df_res.distance.sum(), 'time': df_res.time.sum(), \
                    'commuters': scenario.commuters, 'minDate': minDate, 'maxDate': maxDate, 'departures': scenario.departures, \
                    'tseries': list(tseries_lst), 'max': max.to_dict(orient='records')[0], 'mean': mean.to_dict()})

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