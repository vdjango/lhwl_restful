/*
 * @Author: Marte
 * @Date:   2018-04-10 16:20:27
 * @Last Modified by:   Marte
 * @Last Modified time: 2018-05-08 18:44:20
 * 用于Ajax请求认证
 */

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
//var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});



/* 废弃 */
function setPOST(url, data, error) {
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        token: getCookie('csrftoken'),
        data: data,
        success: function(callback) {
            if (callback['code'] == 200) {
                location.reload();
            } else {
                console.log(callback['code']);
                var html = '<div class="alert alert-warning alert-dismissible">' +
                    '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
                    '<h4><i class="icon fa fa-warning"></i>' + callback[callback['state']] + '</h4></div>';
                document.getElementById(error).innerHTML = html;
            };
        },
        error: function(callback) {
            console.log(callback);
            console.log(callback['code']);
            var html = '<div class="alert alert-warning alert-dismissible">' +
                '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' +
                '<h4><i class="icon fa fa-warning"></i> 啊偶，提交内容失败了！</h4></div>';
            document.getElementById('error').innerHTML = html;
        }
    })
}