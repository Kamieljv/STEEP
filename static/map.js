// Make sure the map's height is equal to the window height
var map = null;

$(document).ready(function (e) {
    var container = $('#map')

    function resizeIFrame(object) {
        object.height(window.innerHeight);
    };
    resizeIFrame(container);

    $(window).on('resize', function() {
        resizeIFrame(container);
    });

    // define Leaflet Map
    map = L.map('map').setView([51.505, -0.09], 14);

    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    //add a route
    var segment1 = [100, 40]
    var segment2 = [105, 45]
    var segment3 = [110, 55]
    var geojsonRoute = [{
        "type": "Feature",
        "properties": {"speed": "low"},
        "geometry": {
            "type": "LineString",
            "coordinates": [segment1, segment3]
        }
    }, {
        "type": "Feature",
        "properties": {"speed": "high"},
        "geometry": {
            "type": "LineString",
            "coordinates": [segment2]
        }
    }];

    var myStyle1 = {
    "color": "#f17202",
    "weight": 5,
    "opacity": 0.65
    };
    var myStyle2 = {
    "color": "#020ef1",
    "weight": 10,
    "opacity": 0.65
    };
    L.geoJSON(geojsonRoute, {
        style: function (feature) {
            switch (feature.properties.speed) {
                case "low": return myStyle1;
                case "high": return myStyle2
            }
        }
    }).addTo(map);
});