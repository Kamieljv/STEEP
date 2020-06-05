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
});

function addr_search() {
    var inp = document.getElementById("addr");
    $.getJSON('http://nomatin.openstreetmap.org/search?format=json&limit=5&q=' + inp.value, function(data))
    };

function addRoute(map, route) {
    /*
    Function that adds a route to the Leaflet map
    map: a Leaflet object
    route: GeoJSON object
    */

    // Define plot styles
    var slow = {
        "color": "#f55142",
        "weight": 5,
        "opacity": 0.8
    };
    var moderate = {
        "color": "#fcbd00",
        "weight": 10,
        "opacity": 0.8
    };
    var fast = {
        "color": "#74f533",
        "weight": 15,
        "opacity": 0.8
    }
    // define multiline object with specific styling
    var multiline = L.geoJSON(route, {
        style: function (feature) {
            var speed = feature.properties.speed;
            switch (true) {
                case (speed <= 50): return slow;
                case (speed <= 80): return moderate;
                case (speed > 80): return fast;
            }
        }
    });
    multiline.addTo(map);
    // pan to multiline object
    map.fitBounds(multiline.getBounds());

}