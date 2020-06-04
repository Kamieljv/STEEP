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