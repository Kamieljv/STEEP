// Initialize variables
var map = null;
var startMarker = null;
var destMarker = null;
var routeLayer = null;
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
            placeMarker(lat, lon, field.name)
        }
    });
}

function placeMarker(lat, lon, type) {
    var location = new L.LatLng(lat, lon);
    var bounds = new L.LatLngBounds();

    if (type == 'start') {
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
    map.fitBounds(bounds, {padding: [30, 30]});
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

// add min and max possible values for emission factor
var minEmissionFactor = 0;
var maxEmissionFactor = 0.3;

var colorFunction = new L.HSLHueFunction(new L.Point(minEmissionFactor, 120), new L.Point(maxEmissionFactor, 20), { outputSaturation: '100%', outputLuminosity: '45%'});

function addRoute(map, route) {
    /*
    Function that adds a route to the Leaflet map
    map: a Leaflet object
    route: GeoJSON object
    */
    // remove old line from
    if (routeLayer != null) {
        map.removeLayer(routeLayer);
    }

    //route.features[3].properties['emissions'] = 200;
    console.log(route);

    routeLayer = new L.ChoroplethDataLayer(route, {
        recordsField: 'features',
        locationMode: L.LocationModes.GEOJSON,
        layerOptions: {
            color: "#000000",
            fillOpacity: 0.7,
            opacity: 1,
            weight: 5,
        },
        displayOptions: {
            'properties.co2_fac': {
                displayName: 'Emission factor CO2',
                color: colorFunction
            },
            'properties.emissions': {
                displayName: 'Emission'
            }
        },
        tooltipOptions: {
            iconSize: new L.Point(80, 55),
            iconAnchor: new L.Point(-10, 80)
        }
    });
    var legendControl = new L.Control.Legend();
    legendControl.addTo(map);
    map.addLayer(routeLayer);
    map.fitBounds(routeLayer.getBounds());
}

function showReport(emissions, distance, time, departure) {
    var em = Math.round(emissions * 100) / 100 // round to 2 decimals
    $('#report').empty();
    $('#report').append('<h4>Calculation Results</h4>');
    $('#report').append('<p><b>Route Emissions:</b> ' + em + ' kg CO2');
    $('#report').append('<p><b>Distance:</b> ' + distance / 1000 + ' km');
    $('#report').append('<p><b>Trip time:</b> ' + secondsToHms(time));
    $('#report').append('<p><b>Departure time:</b> ' + departure);

    $('#report').show();
}

function secondsToHms(d) {
    d = Number(d);
    var h = Math.floor(d / 3600);
    var m = Math.floor(d % 3600 / 60);
    var s = Math.floor(d % 3600 % 60);

    var hDisplay = h > 0 ? h + (h == 1 ? " hour, " : " hours, ") : "";
    var mDisplay = m > 0 ? m + (m == 1 ? " minute, " : " minutes, ") : "";
    var sDisplay = s > 0 ? s + (s == 1 ? " second" : " seconds") : "";
    return hDisplay + mDisplay + sDisplay;
}