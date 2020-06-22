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