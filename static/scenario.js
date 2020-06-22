// initialize date-range picker
$('#date-range').flatpickr({
        mode: "range",
        minDate: "today",
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