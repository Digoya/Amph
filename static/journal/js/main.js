function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var csrftoken = $.cookie('csrftoken');

function subscribeOn(id, elem) {
    if ($(elem).attr('id') === 'subscribe') {
        $.ajax({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: "/ajax/",
                type: "POST",
                data: {
                    function: 'subscribe',
                    author: id
                },
                success: function (data) {
                    $('#subscribe').hide();
                    $('#unsubscribe').show();
                }
            }
        )
    } else if ($(elem).attr('id') === 'unsubscribe') {
        $.ajax({
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                },
                url: "/ajax/",
                type: "POST",
                data: {
                    function: 'unsubscribe',
                    author: id
                },
                success: function (data) {
                    $('#unsubscribe').hide();
                    $('#subscribe').show();
                }
            }
        )
    }
}

// $(document).ready(function () {
//     $('#subscribe').click(function () {
//
//     });
// });

