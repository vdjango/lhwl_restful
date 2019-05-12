$('.fa.fa-level-up.set_level').on('click', function(event) {
    event.preventDefault();
    /* Act on the event */

    $('#level_id').val($(this).attr('value'));

    $.ajax({
        url: '/path/to/file',
        type: 'GET',
        dataType: 'json',
        data: {param1: 'value1'},
    })
    .done(function() {
        console.log("success");
    })
    .fail(function() {
        console.log("error");
    })
    .always(function() {
        console.log("complete");
    });


});