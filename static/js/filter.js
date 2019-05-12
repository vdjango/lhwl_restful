/**
 *
 * @authors Marte (iqianduan@126.com)
 * @date    2018-05-07 22:18:54
 * @version $Id$
 */

var result = "/search/?";

//根据参数名获得该参数  pname等于想要的参数名
function getParam(pname) {

    var params = location.search.substr(1); //  获取参数 平且去掉？
    var ArrParam = params.split('&');
    if (ArrParam.length == 1) {
        //只有一个参数的情况
        return params.split('=')[1];
    } else {
        //多个参数参数的情况
        for (var i = 0; i < ArrParam.length; i++) {
            if (ArrParam[i].split('=')[0] == pname) {
                return ArrParam[i].split('=')[1];
            }
        }
    }
}


/*
$(function() {
     var mao = $("#" + getParam("m")); //获得锚点
     if (mao.length > 0) {//判断对象是否存在
         var pos = mao.offset().top;
         var poshigh = mao.height();
         $("html,body").animate({ scrollTop: pos-poshigh-30 }, 2000);
     }
 });
*/


$(function() {

    $("#filter a").click(function() {
        $(this).parents("dl").children("dd").each(function() {
            $(this).children("div").children("a").removeClass("seled");
        });

        $(this).attr("class", "seled");
        var aax = RetSelecteds();
        window.location.href = aax;
    });

    var ht = $("#filter a[class='seled']");
    var params = location.search.substr(1); //  获取参数 平且去掉？
    var ArrParam = params.split('&');

    if (ArrParam.length <= 1) {
        $("#filter dt+dd a").attr("class", "seled");
    };

    var html = '<li><a><i class="fa fa-firefox"></i> 全部结果</a></li>';

    if (ArrParam.length > 1) {
        console.log(ArrParam.length);
        for (var i = 1; i < ArrParam.length; i++) {
            var va = ArrParam[i].split('=');
            var search = ArrParam[i].split('search');
            if (va[1]) {
                var va_value = va[1].split('[.!@]');
                var bid = document.getElementById(va_value[0]);

                if (bid) {
                    bid.className = "seled";
                    if (va_value[1].length > 0) {
                        html += '<li><a href="#">' + va_value[1] + '</a></li>';
                    };
                };
            };
            if (search.length > 1) {
                search = search[1].split('=')[1];
                html += '<li><a href="#">' + search + '</a></li>';
            };

            document.getElementById('search_all').innerHTML = decodeURIComponent(html);
        };
    } else {
        var search = params.split('search');
        if (search[1].length > 1) {
            search = search[1].split('=')[1];
            html += '<li><a href="#">' + search + '</a></li>';
        };
        document.getElementById('search_all').innerHTML = decodeURIComponent(html);
    };
});

function RetSelecteds() {
    var paramss = location.search.substr(1); //  获取参数 平且去掉？
    var search = paramss.split('search');
    var search_ok = paramss.split('searback');

    $("#filter a[class='seled']").each(function() {
        for (var i = 0; i < $(this).length; i++) {
            var value = $(this)[i].getAttribute('value');
            var url = $(this)[i].getAttribute('url');
            var id = $(this)[i].getAttribute('id');
            var ArrParam = url.split('=')[0];
            url = '&' + url + id + '[.!@]' + value;
            result += url;
        };
    });
    if (search.length > 1) {
        search = search[1].split('=')[1];
        result += '&search=' + search;
    };

    search_ok = document.getElementById('search_ok').value
    result += '&searback=' + search_ok;
    console.log("search_ok " + search_ok);

    return result;
}



/**********/