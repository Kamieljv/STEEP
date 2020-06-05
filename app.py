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
    return render_template('home.html')


@app.route('/relocate', methods=['POST'])
def relocate():
    lat = request.form['latitude']
    lon = request.form['longitude']
    return json.dumps({'type':'relocate', 'lat':lat, 'lon':lon})

@app.route('/start_dest', methods=['POST'])
def start_dest():
    start = request.form['Start']
    dest = request.form['Destination']
    return json.dumps({'type':'enter', 'start':start, 'dest':dest})

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