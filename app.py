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


@app.route('/calculate_route', methods=['POST'])
def calculate_route():
    start = request.form['start']
    dest = request.form['dest']
    departure = request.form['departure']
    startCoords = request.form['start-coords']
    destCoords = request.form['dest-coords']
    fuel = request.form['fuel']
    segment = request.form['segment']
    standard = request.form['standard']
    return json.dumps({'start':start, 'startCoords':startCoords, 'destCoords':destCoords, 'dest':dest, 'departure':departure, 'fuel':fuel, 'segment':segment, 'standard':standard})


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

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/help', methods=['GET'])
def help():
    return render_template('help.html')


if __name__ == '__main__':
    app.run(debug=True)