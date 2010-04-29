var form_id = '#edit_business_card_form'


function bind_calendar_widget () {
    var calendar = $("#id_birth_date")
    calendar.datepicker({
        dateFormat: 'yy-mm-dd',
        changeYear: true,
        yearRange: '1900:c'
    });
};


$(document).ready(function() {
    var options = {
                    target:        $(form_id),
                    dataType:      "html",
                    url:           '/edit/form/',
                    beforeSubmit:  disable_form,
                    success:       treat_response
    };

    $(form_id).ajaxForm(options);
    bind_calendar_widget();
});


function disable_form () {
    var items = $(form_id + ' input, textarea');

    $.each(items, function(index, item) {
        item.disabled = true;
    });

    $('#progress').css('visibility', 'visible');
};


function treat_response (data) {
    $(form_id).html(data);
    bind_calendar_widget();
};
