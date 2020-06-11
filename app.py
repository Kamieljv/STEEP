""" app.py

    Required packages:
    - flask


    Usage:

    Start the flask server by running:

        $ python app.py

    And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""

from flask import Flask, render_template, request, json
import src.vehicle_config

# Load vehicle configuration class
VehicleConfig = src.vehicle_config.VehicleConfig()


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    """Sets vehicle parameter options and renders home-page."""
    fuels = VehicleConfig.fuels
    segments = VehicleConfig.segments
    standards = VehicleConfig.standards
    return render_template('home.html', fuels=fuels, segments=segments, standards=standards, title="Home")


@app.route('/calculate_route', methods=['POST'])
def calculate_route():
    """Gets route configuration; calculates route; returns route to view as JSON."""
    start = request.form['start']
    dest = request.form['dest']
    departure = request.form['departure']
    startCoords = request.form['start-coords']
    destCoords = request.form['dest-coords']
    fuel = request.form['fuel']
    segment = request.form['segment']
    standard = request.form['standard']
    return json.dumps({'start':start, 'startCoords':startCoords, 'destCoords':destCoords, 'dest':dest, 'departure':departure, 'fuel':fuel, 'segment':segment, 'standard':standard})

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