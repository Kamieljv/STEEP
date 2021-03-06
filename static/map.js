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
var TWResponse = null;

$(document).ready(function (e) {
    var container = $('#map')
    if (container.length === 0) {
        console.log('No map on page');
        return
    }

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
                displayName: 'Emission factor (kgCO2/km)',
                color: colorFunction
            },
            'properties.emissions': {
                displayName: 'Emission',
                excludeFromLegend: true,
            }
        },
        tooltipOptions: {
            iconSize: new L.Point(80, 55),
            iconAnchor: new L.Point(-10, 80)
        },
        showLegendTooltips: false,
        onEachRecord: function(layer, record) {
            layer.bindTooltip('<b>kg CO2/km:</b> ' + record.properties.co2_fac + '<br/>'
                            + '<b>kg CO2:</b> ' + record.properties.emissions);
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
     $('#report').empty();
    $('#report').append('<h4>Calculation Results</h4>');
    $('#report').append('<p><b>Route Emissions:</b> ' + em * 1000 + ' g CO2');
    $('#report').append('<p><b>Distance:</b> ' + distance / 1000 + ' km');
    $('#report').append('<p><b>Trip time:</b> ' + secondsToHms(time));
    $('#report').append('<p><b>Departure time:</b> ' + departure);
    $('#report').show();

}

function showTimewindow(response) {
    TWResponse = response; // store response as global variable

    $('#report').empty();
    $('#report').append('<h4>Calculation Results</h4>');
    var defaultKey = null;
    for ( d= 0; d < Object.keys(response).length; d++) {
        if (response['route'+d].default === 'true') {
            defaultKey = 'route'+d;
        }
    }
    route = JSON.parse(response[defaultKey].route);
    addRoute(map, route); // add default route to map

    let defaultEmissions = response[defaultKey] ? response[defaultKey].emissions * 1000 : 0;
    response[defaultKey].rightWidth = 0;
    response[defaultKey].leftWidth = 0;

    diffs = [] // define a list of emission differences
    // Loop through results to calculate maximum emission difference
    for (i = 0; i < Object.keys(response).length; i++) {
        em = response['route'+i].emissions * 1000; // convert from kg to g
        let diff = Math.round(Number(em - defaultEmissions) * 100) / 100;
        diffs.push(diff);
    }

    // Loop through results to add report cards
    for (i = 0; i < Object.keys(response).length; i++) {
        var item = response['route'+i];
        item.emissions = item.emissions * 1000;
        if (item.default !== 'true') {
            width = diffs[i];
            if (width < 0) {
                item.leftWidth = width * -1;
            } else {
                item.rightWidth = width;
            }
        }
        // Calculate percentages of the maximum emission difference
        item.leftPerc = item.leftWidth / Math.max.apply(null, diffs.map(Math.abs)) * 100;
        item.rightPerc = item.rightWidth / Math.max.apply(null, diffs.map(Math.abs)) * 100;
        // Fetch html and append to report section
        let resultHtml = getItemHtml(item, i);
        $('#report').append(resultHtml)
    };

    $('#report').show();

    // Auto-scroll to report
    $('#controls').animate({
                    scrollTop: $("#report").offset().top
    }, 500);
}

function getItemHtml(itemInfo, index) {
    let em = Math.round(itemInfo.emissions * 100) / 100  // round to 2 decimals
    let distance = itemInfo.distance / 1000;
    let time = secondsToHms(itemInfo.time);
    let def = itemInfo.default === "true"
    let resultHtml = `<div class="result_card ${def ? 'chosen' : ''}" data-index="${i}">`
         + `<div class="card_info">`
         +      `<div class="card_info_text padding_bottom">Route Emissions: ${em} g CO2</div>`
         +      `<div class="card_info_text padding_bottom">Distance: ${distance} km</div>`
         +      `<div class="card_info_text padding_bottom">Trip time: ${time}</div>`
         +      `<div class="card_info_text">Departure time: ${itemInfo.departure}</div>`
         + `</div>`
         + '<div class="card_div">'
         +  '<div class="card_img">'
         +      `<div class="img_left">`
         +          `<div class="bar_left" style="width: ${itemInfo.leftPerc ? itemInfo.leftPerc : 0}%;"></div>`
         +      `</div>`
         +      `<div class="img_center"></div>`
         +      `<div class="img_right">`
         +          `<div class="bar_right" style="width: ${itemInfo.rightPerc ? itemInfo.rightPerc : 0}%;"></div>`
         +      `</div>`
         +  '</div>'
         +  `<div class="bottom_text">${itemInfo.leftWidth ? '-' : itemInfo.rightWidth ? '+' : ''}${itemInfo.leftWidth || itemInfo.rightWidth || em} g</div>`
         + '</div>'
         +'</div>';
    return resultHtml;
}

$(document).on('click', '.result_card:not(.chosen)', function(e) {
    e.preventDefault();
    var index = this.dataset.index;
    var route = JSON.parse(TWResponse['route'+index].route);
    addRoute(map, route);
    $('.result_card.chosen').removeClass('chosen');
    $(this).addClass('chosen');
});


function secondsToHms(d) {
    d = Number(d);
    var h = Math.floor(d / 3600);
    var m = Math.floor(d % 3600 / 60);
    var s = Math.floor(d % 3600 % 60);

    var hDisplay = h > 0 ? h + (h == 1 ? " hr, " : " hrs, ") : "";
    var mDisplay = m > 0 ? m + (m == 1 ? " min, " : " mins, ") : "";
    var sDisplay = s > 0 ? s + (s == 1 ? " sec" : " sec") : "";
    return hDisplay + mDisplay + sDisplay;
}