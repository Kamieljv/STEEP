
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
                if (data.type == 'relocate') {
                    map.setView(new L.LatLng(data.lat, data.lon), 8);
                } else if (data.type == 'addroute') {
                    addRoute(map, data.route);
                } else {
                    console.log(data);
                }
            },
            error: function(error) {
                console.log(error);
            }
        });

    }
    else {
        // first, scan the page for labels, and assign a reference to the label from the actual form element:
        var labels = $(form).find('label');

        // then find all invalid input elements (form fields)
        var invalidList = form.querySelectorAll(':invalid');

        if ( typeof invalidList !== 'undefined' && invalidList.length > 0 ) {
            // errors were found in the form (required fields not filled out)

            // for each invalid input element (form field) return error
            for (var item of invalidList) {
                var errorContainer = item.nextElementSibling;
                $(item.nextElementSibling).html(item.nextElementSibling.dataset.error);
                $(errorContainer).show()
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


$('form button').click(function(event){
    // Prevent redirection with AJAX for contact form
    event.preventDefault();

    // First check if the start and destination are entered,
    // because in that case the input has to be geocoded by Nomatim first
    if (this.id == 'dest-btn' || this.id == 'start-btn' ) {

        var objID = $(this).attr('for');
        var field = $('#' + objID)[0];
        locationSearch(field.value, field);

    } else {

        var form = $(this).parents('form')[0];
        var url = form.action;
        var type = form.method;
        var formData = new FormData(form);

        send_form(form, url, type, formData);

     }
});
