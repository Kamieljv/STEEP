var error = "";

$(document).ajaxComplete(function(event, request, settings) {
  $('.loader').hide();
});

function send_form(form, url, type, formData) {
    // form validation and sending of form items

    if (!isFormDataEmpty(form, formData) && checkTimes(form)) { // checks if form is empty
        event.preventDefault();
        $('.loader').show();

        // make AJAX call
        $.ajax({
            url: url,
            data: formData,
            type: type,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.hasOwnProperty('route')) {
                    route = JSON.parse(response.route);
                    addRoute(map, route);
                    showReport(response.emissions, response.distance, response.time, response.departure);
                } else if (response.hasOwnProperty('route0')) {
                    route = JSON.parse(response.route2.route);
                    addRoute(map, route);
                    showTimewindow(response);
                } else {
                    if (response.hasOwnProperty('error')) {
                        $('#form_error').html(response.error).show();
                    } else {
                        showScenario(response);
                    }
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(thrownError);
              }
        });

    } else {
        if (error.length != 0) {
            $('#form_error').html(error).show();
            error = "";
        }
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
    if (status) {
        error = "Please fill in all required fields.";
    }

    return status;
}

function checkTimes(form) {
    // check if the #return-time element exists in the form
    if ($(form).find('#return-time').length != 0) {
        if ($('#departure-time').val() >= $('#return-time').val()) {
            error = "The departure time has to be before the return time."
            $('#departure-time').toggleClass('is-invalid', true).toggleClass('is-valid', false);
            $('#return-time').toggleClass('is-invalid', true).toggleClass('is-valid', false);
            return false;
        }
    }

    return true;
}

$('#calculate-btn').click(function(event){
    // Prevent redirection with AJAX for contact form
    event.preventDefault();

    // hide Report
    $('#report').hide();
    // clear form error
    $('#form_error').empty().hide();
    // hide scenario report
    $('#scenario-report').hide();

    var form = $(this).parents('form')[0];
    var url = form.action;
    var type = form.method;
    var formData = new FormData(form);

    // clear all invalids
    for (var input of $(form).find('input, select')) {
        $(input).toggleClass('is-invalid', false).toggleClass('is-valid', false);
    }

    send_form(form, url, type, formData);
});

$('form button.btn-loc').click(function(event){
    // Prevent redirection with AJAX for contact form
    event.preventDefault();

    var objID = $(this).attr('for');
    // Geocode the input with Nomatim
    locationSearch($('#' + objID)[0].value, $('#' + objID)[0], $('#'+objID+'-coords')[0]);
});

// Clear validation class on keyup/click
$(document).on('keyup', 'input', function(e) {
    $(this).toggleClass('is-invalid', false).toggleClass('is-valid', false);
});
$(document).on('click', 'input, select', function(e) {
    $(this).toggleClass('is-invalid', false).toggleClass('is-valid', false);
});

// Search location on enter
$(document).on('keyup', '#start, #dest', function(e) {
    if (e.keyCode === 13) {
        e.preventDefault();
        $(this).parent().parent().next().find('input').focus();
    }
});
// Search location on unfocus
$(document).on('focusout', '#start, #dest', function(e) {
    e.preventDefault();
    locationSearch(this.value, this, $('#'+this.id+'-coords')[0]);
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

$('#swap-btn').click(function (e) {
    var dest = $('#dest').val();
    var destCoords = $('#dest-coords').val();
    $('#dest').val($('#start').val());
    $('#start').val(dest);
    $('#start-btn').click();
    $('#dest-btn').click();
});