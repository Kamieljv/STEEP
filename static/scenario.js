$('.btn-manual-entry').click(function(e) {
    $(this).addClass('active');
    $('.btn-excel-entry').removeClass('active');
    $('#excel-container').hide();
    $('#manual-container').show();
    $('html, body').animate({
                    scrollTop: $("#manual-container").offset().top
    }, 500);
});
$('.btn-excel-entry').click(function(e) {
    $(this).addClass('active');
    $('.btn-manual-entry').removeClass('active');
    $('#manual-container').hide();
    $('#excel-container').show();
    $('html, body').animate({
                    scrollTop: $("#excel-container").offset().top
    }, 500);
});

// initialize date-range picker
$('#date-range').flatpickr({
        mode: "range",
        minDate: new Date().fp_incr(1),
        dateFormat: "Y-m-d",
    });

$(function(){
    $('#weekdays').weekdays({
        selectedIndexes: [0, 1, 2, 3, 4],
        days: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    });
});

$(document).on('click', '#weekdays', function(e) {
    var weekdays = [];
    for (var day of $(this).children().children()) {
        if ($(day).hasClass('weekday-selected')) {
            weekdays.push(day.dataset.day)
        }
    }
    $('#weekdays-input').val(weekdays);
});

$('#departure-time, #return-time').flatpickr({
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true
});

function showScenario(response) {
    $('#scenario-report').show();
    var t = response.tseries.map(function(val){
        return math.round(val * response.commuters,3)
    });
    t = math.reshape(t, [t.length/24, 24]);
    t = math.transpose(t) // transpose the matrix for the heatmap to plot correctly
    var dates = getDaysArray(response.minDate, response.maxDate);
    var days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
    dates = dates.map(function(d){
                return days[d.getDay()]+" "+d.getDate()+" "+d.toLocaleString('default', { month: 'short' });
            });

    var data = { labels: dates, datasets: [] };
    for (i = 0; i < t.length; i++) {
        data.datasets.push({label: i+'-'+(i+1)+'h', data: t[i]});
    }

    var ctx = document.getElementById('heatmap').getContext('2d');
    var options = {
        rounded: false,
        showLabels: false,
        tooltipTemplate: "<%= xLabel %> | <%= yLabel %> : <%= value %> kgCO2",
        colors: [ "rgba(220,220,220,0.9)", "rgba(68, 82, 102, 1)"],
        colorHighlightMultiplier: 0.85,
        legendTemplate :'<div class="<%= name.toLowerCase() %>-legend">'+
                            '<div class="row">' +
                                '<div class="col-12">' +
                                    '<h5>Legend</h5>' +
                                '</div>' +
                            '</div>' +
                            '<div class="row">' +
                                '<div class="col-12 d-flex flex-column text-center">' +
                                    '<i>in kgCO2</i>' +
                                    '<span class="<%= name.toLowerCase() %>-legend-min">'+
                                    '<%= min %>'+
                                    '</span>'+
                                    '<span class="<%= name.toLowerCase() %>-legend-box" style="background-image: linear-gradient(<%= options.colors[0] %>, <%= options.colors[1] %>);">'+
                                    '</span>'+
                                    '<span class="<%= name.toLowerCase() %>-legend-max">'+
                                    '<%= max %>'+
                                    '</span>'+
                                '</div>' +
                            '</div>' +
                        '</div>'
    }
    var chart = new Chart(ctx).HeatMap(data, options);
    var legend = chart.generateLegend();
    $('#chart-legend').html(legend);

    // Remove table rows if any
    $('#scenario-table').find('tbody').remove();
    // Add statistics to table
    statsTable(response)

    $('html, body').animate({
                    scrollTop: $("#scenario-report").offset().top
    }, 500);

}

function statsTable(response) {
    $('#scenario-table').append(
        '<tbody>' +
            '<tr>' +
                '<th scope="row">Emissions (kgCO2)</th>' +
                '<td>'+ math.round(response.emissions * response.commuters, 3) +'</td>' +
                '<td>'+ math.round(response.emissions, 3) +'</td>' +
                '<td>'+ math.round(response.max.emissions, 3) +'</td>' +
                '<td>'+ math.round(response.mean.emissions, 3) +'</td>' +
            '</tr>' +
            '<tr>' +
                '<th scope="row">Distance (km)</th>' +
                '<td>'+ math.round(response.distance * response.commuters / 1000, 3) +'</td>' +
                '<td>'+ math.round(response.distance / 1000, 3) +'</td>' +
                '<td>'+ math.round(response.max.distance / 1000, 3) +'</td>' +
                '<td>'+ math.round(response.mean.distance / 1000, 3) +'</td>' +
            '</tr>' +
            '<tr>' +
                '<th scope="row">Commute time</th>' +
                '<td>'+ secondsToHms(response.time * response.commuters) +'</td>' +
                '<td>'+ secondsToHms(response.time) +'</td>' +
                '<td>'+ secondsToHms(response.max.time) +'</td>' +
                '<td>'+ secondsToHms(response.mean.time) +'</td>' +
            '</tr>' +
        '</tbody>'
    );
}

var getDaysArray = function(start, end) {
    end = new Date(end);
    for(var arr=[],dt=new Date(start); dt<=end; dt.setDate(dt.getDate()+1)){
        arr.push(new Date(dt));
    }
    return arr;
};