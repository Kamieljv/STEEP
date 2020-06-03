""" flask_example.py

    Required packages:
    - flask
    - folium

    Usage:

    Start the flask server by running:

        $ python flask_example.py

    And then head to http://127.0.0.1:5000/ in your browser to see the map displayed

"""

from flask import (Flask, render_template, request)

import folium

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    start_coords = (46.9540700, 142.7360300)

    if request.method == 'POST':
        start_coords = (request.form["x"], request.form["y"])

    folium_map = folium.Map(location=start_coords, zoom_start=14)._repr_html_()

    return render_template('home.html', map=folium_map, form=None)


if __name__ == '__main__':
    app.run(debug=True)

