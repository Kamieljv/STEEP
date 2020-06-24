// Initialize variables
var map = null;
var startMarker = null;
var destMarker = null;
var multiline = null;
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

    // remove old line from
    if (multiline != null) { map.removeLayer(multiline); }

    // Define plot styles
    var red = {
        "color": "#f55142",
        "weight": 5,
        "opacity": 0.8
    };
    var orange = {
        "color": "#fcbd00",
        "weight": 10,
        "opacity": 0.8
    };
    var green = {
        "color": "#74f533",
        "weight": 15,
        "opacity": 0.8
    }
    // define multiline object with specific styling
    multiline = L.geoJSON(route, {
        style: function (feature) {
            var em_fac = feature.properties.em_fac;
            switch (true) {
                case (em_fac <= 1.5): return green;
                case (em_fac <= 2): return orange;
                case (em_fac > 2): return red;
            }
        }
    });
    multiline.addTo(map);
    // pan to multiline object
    map.fitBounds(multiline.getBounds());
}

function showReport(emissions, distance, time, departure) {
    console.log('Put old showReport function here.');
}

function showTimewindow(response) {

    $('#report').empty();
    $('#report').append('<h4>Calculation Results</h4>');
    let firstEmissions = 0;
    for (i = 0; i < Object.keys(response).length; i++) {
        var item = response['route'+i]
        if (i === 0) {
            firstEmissions = item.emissions;
            item.rightWidth = 0;
            item.leftWidth = 0;
        } else {
            let width = Number(item.emissions - firstEmissions).toFixed(2);
            width = Number(width);
            if (width > 0) {
                item.leftWidth = width;
            } else {
                item.rightWidth = width * -1;
            }
        }
        let resultHtml = getItemHtml(item);
        console.log(resultHtml, 'resultHtml');
        $('#report').append(resultHtml)
    };
    $('#report').show();
}

function getItemHtml(itemInfo) {
    let em = Math.round(itemInfo.emissions * 100) / 100 // round to 2 decimals
    let distance = itemInfo.distance / 1000;
    let time = secondsToHms(itemInfo.time);
    let resultHtml = `<div class="result_card">`
         + `<div class="card_info">`
         +      `<div class="card_info_text padding_bottom">Route Emissions: ${em} kg CO2</div>`
         +      `<div class="card_info_text padding_bottom">Distance: ${distance} km</div>`
         +      `<div class="card_info_text padding_bottom">Trip time: ${time}</div>`
         +      `<div class="card_info_text">Departure time: ${itemInfo.departure}</div>`
         + `</div>`
         + '<div class="card_div">'
         +  '<div class="card_img">'
         +      `<div class="img_left" style="width: ${itemInfo.leftWidth ? itemInfo.leftWidth : 0}px"></div>`
         +      `<div class="img_center"></div>`
         +      `<div class="img_right" style="width: ${itemInfo.rightWidth ? itemInfo.rightWidth : 0}px"></div>`
         +  '</div>'
         +  `<div class="bottom_text">${itemInfo.leftWidth ? '+' : itemInfo.rightWidth ? '-' : ''}${itemInfo.leftWidth || itemInfo.rightWidth || em}</div>`
         + '</div>'
         +'</div>';
    return resultHtml;
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