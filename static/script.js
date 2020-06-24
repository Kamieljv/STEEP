
function send_form(form, url, type, formData) {
    // form validation and sending of form items

    if (!isFormDataEmpty(form, formData)) { // checks if form is empty
        event.preventDefault();
        // make AJAX call
        $.ajax({
            url: url,
            data: formData,
            type: type,
            processData: false,
            contentType: false,
            success: function(response) {
                if(response.hasOwnProperty('route')){
                    route = JSON.parse(response.route);
                    addRoute(map, route);
                    showReport(response.emissions, response.distance, response.time, response.departure);
                } else {
                    route = JSON.parse(response.route2.route);
                    addRoute(map, route);
                    showTimewindow(response);
                }
            },
            error: function(error) {
                console.log(error);
            }
        });

    }
}

function isFormDataEmpty(form, formData) {
    // checks for all values in formData object if they are empty
    var status = false;
    for (var [key, value] of formData.entries()) {
        if (key != 'csrf_token') {
            if (value == '' || value == []) {
                var id = ($('#'+key)[0].type === 'hidden')? $('#'+key).prev()[0].id : key;
                $('#'+id).toggleClass('is-invalid', true).toggleClass('is-valid', false);
                status = true;
            }
        }
    }
    // also explicitly check select inputs
    for (field of $(form).find('select')) {
        if (!$(field).val()) {
            $(field).toggleClass('is-invalid', true).toggleClass('is-valid', false);
            status = true;
        }
    }
    return status;
}

$('#calculate-btn').click(function(event){
    // Prevent redirection with AJAX for contact form
    event.preventDefault();

    // hide Report
    $('#report').hide()

    var form = $(this).parents('form')[0];
    var url = form.action;
    var type = form.method;
    var formData = new FormData(form);

    send_form(form, url, type, formData);
});

$('form button.btn-loc').click(function(event){
    // Prevent redirection with AJAX for contact form
    event.preventDefault();
    // Define parameters
    var objID = $(this).attr('for');
    var field = $('#' + objID)[0];
    var coordField = $(field).next()[0];
    // Geocode the input with Nomatim
    locationSearch(field.value, field, coordField);
});

// Clear validation class on keyup/click
$(document).on('keyup', 'input', function(e) {
    $(this).toggleClass('is-invalid', false).toggleClass('is-valid', false);
});
$(document).on('click', '#departure', function(e) {
    $(this).toggleClass('is-invalid', false).toggleClass('is-valid', false);
});

// Search location on enter
$(document).on('keyup', '#start, #dest', function(e) {
    if (e.keyCode === 13) {
        e.preventDefault();
        $('#' + this.id + '-btn').click();
        $(this).parent().parent().next().find('input').focus();
    }
});

// initialize date-time picker
$('#departure').flatpickr({
    'enableTime': true,
    'minDate': new Date(),
    'dateFormat': "Y-m-d H:i",
    'time_24hr': true
    });

// Set current date and time on button click
$('#today-btn').click(function(e) {
    // clear departure validation class
    $('#departure').toggleClass('is-invalid', false).toggleClass('is-valid', false);
    // get date
    var today = new Date();
    var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    var time = today.getHours() + ":" + today.getMinutes();
    var dateTime = date+' '+time;
    $('#departure')[0].value = dateTime;
});

$(document).on('change', '#fuel, #segment, #standard', function (e) {
    event.preventDefault();

    var getUrl = window.location;
    var url = getUrl.protocol + "//" + getUrl.host + '/getoptions';
    var data = {'fuel': $('#fuel').val()};
    var currID = this.id;
    // include segment if not changing fuel selector
    data['segment'] = (currID != 'fuel')? $('#segment').val() : "";
    if (currID == 'fuel') {
        $('.v-param:not(#fuel)').prop('disabled', true); // disable next fields
    }

    // make AJAX call
    $.ajax({
        url: url,
        data: data,
        type: 'POST',
        success: function(response) {
            for (obj of $('.v-param:not(#'+ currID +')')) {
                if (obj.dataset.idx > $('#'+currID)[0].dataset.idx) {
                    $(obj).empty();
                    $(obj).append('<option value="" disabled selected>Select a ' + obj.id + '</option>');
                    for (opt of response[obj.id]) {
                        var option = $('<option></option>').attr("value", opt).text(opt);
                        $(obj).append(option);
                    }
                    if (obj.dataset.idx - $('#'+currID)[0].dataset.idx === 1) {
                        $(obj).prop('disabled', false);
                    }
                }
            }

        },
        error: function(error) {
            console.log(error);
        }
    });
});