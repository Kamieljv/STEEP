
function send_form(form, url, type, formData) {
    // form validation and sending of form items

    if ( form.checkValidity() && isFormDataEmpty(formData) == false ) { // checks if form is empty
        event.preventDefault();

        // make AJAX call
        $.ajax({
            url: url,
            data: formData,
            type: type,
            processData: false,
            contentType: false,
            success: function(response) {
                data = JSON.parse(response);
                console.log(data);
            },
            error: function(error) {
                console.log(error);
            }
        });

    }
    else {
        // then find all invalid input elements (form fields)
        var invalidList = form.querySelectorAll(':invalid');

        if ( typeof invalidList !== 'undefined' && invalidList.length > 0 ) {
            // errors were found in the form (required fields not filled out)

            // for each invalid input element (form field) return error
            for (var item of invalidList) {
                $(item).toggleClass('is-invalid', true).toggleClass('is-valid', false);
            }
        }
    }
}

function isFormDataEmpty(formData) {
    // checks for all values in formData object if they are empty
    for (var [key, value] of formData.entries()) {
        if (key != 'csrf_token') {
            if (value != '' && value != []) {
                return false;
            }
        }
    }
    return true;
}


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

$('#calculate-btn').click(function(event){
    // Prevent redirection with AJAX for contact form
    event.preventDefault();

    var form = $(this).parents('form')[0];
    var url = form.action;
    var type = form.method;
    var formData = new FormData(form);

    send_form(form, url, type, formData);
});

$(document).on('keyup', 'input', function(e) {
    $(this).toggleClass('is-invalid', false).toggleClass('is-valid', false);
});

// Search location on enter
$(document).on('keyup', '#start, #dest', function(e) {
    if (e.keyCode === 13) {
        e.preventDefault();
        $('#' + this.id + '-btn').click();
    }
});

// initialize date-time picker
$('#departure').flatpickr({
    'enableTime': true,
    'dateFormat': "Y-m-d H:i",
    'time_24hr': true
    });

// Set current date and time on button click
$('#today-btn').click(function(e) {
    var today = new Date();
    var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    var time = today.getHours() + ":" + today.getMinutes();
    var dateTime = date+' '+time;
    $('#departure')[0].value = dateTime;
});