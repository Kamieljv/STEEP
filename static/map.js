// Initialize variables
var map = null;
var startMarker = null;
var destMarker = null;
var greenIcon = L.icon({
    iconUrl: '/static/marker-green.png',
    iconSize: [40, 40],
    iconAnchor: [20, 40],
});
var redIcon = L.icon({
    iconUrl: '/static/marker-red.png',
    iconSize: [40, 40],
    iconAnchor: [20, 40],
});

$(document).ready(function (e) {
    var container = $('#map')

    function resizeIFrame(object) {
        // the navigation bar takes up 56 px
        object.height(window.innerHeight - 56);
    };
    resizeIFrame(container);

    $(window).on('resize', function() {
        resizeIFrame(container);
    });

    // define Leaflet Map
    map = L.map('map', {zoomControl: false}).setView([51.9745, 5.664], 14);
    L.control.zoom({
        position: 'topright'
    }).addTo(map);

    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
});

function locationSearch(locationName, field, coordField) {
    $.getJSON("https://nominatim.openstreetmap.org/search?format=geojson&limit=5&q=" + locationName, function(data) {
        var items = [];
        first_hit = (data['features'].length != 0)? data['features'][0] : null;

        // Process the search result
        $.each(data['features'], function(i, feature) {
            lon = feature['geometry']['coordinates'][0];
            lat = feature['geometry']['coordinates'][1];
            type = feature['geometry']['type'];
            display_name = feature['properties']['display_name'];

            items.push(
                "<li><a href='#' onclick='zoomToFeature(" +
                lat + ", " + lon + ", " + type + ");return false;'>" + display_name +
                '</a></li>'
            );
        });
        // Clear the previous search result in the results div
        $('#results').empty();

        // Add all the search result to the results div
        var isValid = true;
        if (items.length != 0) {
            $('<p>', { html: "Search results:" }).appendTo('#results');
            $('<ul/>', {
                'class': 'my-new-list',
                html: items.join('')
            }).appendTo('#results');
        } else {
            $('<p>', { html: "No results found" }).appendTo('#results');
            // set input field to invalid
            isValid = false;
        }

        // set the input field to valid
        $(field).toggleClass('is-invalid', !isValid).toggleClass('is-valid', isValid)

        if (isValid && first_hit) {
            // set the input field value
            field.value = first_hit['properties']['display_name'];

            // set the result coordinates in the hidden field
            lon = first_hit['geometry']['coordinates'][0];
            lat = first_hit['geometry']['coordinates'][1];
            coordField.value = lat + ", " + lon;

            // place a marker on the leaflet map
            var location = new L.LatLng(lat, lon);
            var bounds = new L.LatLngBounds();

            if (field.name == 'start') {
                if (startMarker) {map.removeLayer(startMarker);}
                startMarker = L.marker(location, {icon: greenIcon}).addTo(map);
                bounds.extend(startMarker.getLatLng());
                if (destMarker) {bounds.extend(destMarker.getLatLng());}
            } else {
                if (destMarker) {map.removeLayer(destMarker);}
                destMarker = L.marker(location, {icon: redIcon}).addTo(map);
                bounds.extend(destMarker.getLatLng());
                if (startMarker) {bounds.extend(startMarker.getLatLng());}
            }

            // pan/zoom to have all current features on screen
            map.fitBounds(bounds);
        }
    });
}
function zoomToFeature(lat, lng, type) {
  var location = new L.LatLng(lat, lng);
  map.panTo(location);

  if (type == 'city' || type == 'administrative') {
    map.setZoom(11);
  } else {
    map.setZoom(13);
  }
}

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
                case (speed <= 20): return slow;
                case (speed <= 80): return moderate;
                case (speed > 80): return fast;
            }
        }
    });
    multiline.addTo(map);
    // pan to multiline object
    map.fitBounds(multiline.getBounds());

}