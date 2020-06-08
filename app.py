""" flask_example.py

    Required packages:
    - flask
    - folium

    Usage:

    Start the flask server by running:

        $ python flask_example.py

    And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""

from flask import Flask, render_template, request, json
import folium

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    fuels = ['Petrol', 'Diesel', 'Petrol Hybrid', 'LPG Bifuel ~ LPG', 'LPG Bifuel ~ Petrol', 'CNG Bifuel ~ Petrol', 'CNG Bifuel ~ CNG']
    segments = ['Mini', 'Small', 'Medium', 'Large-SUV-Executive', '2-Stroke']
    standards = ['Conventional', 'ECE 15/00-01', 'ECE 15/02', 'ECE 15/03', 'ECE 15/04', 'Euro 1', 'Euro 2', 'Euro 3', 'Euro 4',\
                'Euro 5', 'Euro 6', 'Euro 6 2017-2019', 'Euro 6 2020+', 'Euro 6 up to 2016', 'Improved Conventional', 'Open Loop', 'PRE ECE']
    return render_template('home.html', fuels=fuels, segments=segments, standards=standards)


@app.route('/relocate', methods=['POST'])
def relocate():
    lat = request.form['latitude']
    lon = request.form['longitude']
    return json.dumps({'type':'relocate', 'lat':lat, 'lon':lon})

@app.route('/vehicle', methods=['POST'])
def vehicle():
    fuel = request.form['fuel']
    segment = request.form['segment']
    standard = request.form['standard']
    return json.dumps({'type':'vehicle', 'fuel':fuel, 'segment':segment, 'standard':standard})

@app.route('/addsearch', methods=['POST'])
def addsearch():
    start = request.form['Start']
    dest = request.form['Destination']
    return json.dumps({'type':'search', 'start':start, 'dest':dest})

@app.route('/addroute', methods=['POST'])
def addroute():
    with open('static/sample.geojson') as f:
        route = json.load(f)
    return json.dumps({'type':'addroute', 'route':route})

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['Pragma'] = 'no-cache'
    return response


if __name__ == '__main__':
    app.run(debug=True)