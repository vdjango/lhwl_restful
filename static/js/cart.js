/**
 *
 * @authors Marte (iqianduan@126.com)
 * @date    2018-07-07 20:05:35
 * @version $Id$
 */

$(function() {
    var url = '/shopping/CartToolp/';

    function posCart() {
        /* 右上角的购物车，获取购物车商品 */
        $.ajax({
                url: url, //'{% url "shop:CartToolp" %}',
                type: 'GET',
                dataType: 'json',
                data: {},
            })
            .done(function(data) {
                if (data.code == 200) {
                console.log(data);
                    var html = '';
                    for (var i = 0; i < data.data.Cart.length; i++) {
                        html += '<div class="col-md-12 box-list">' +
                            '   <div class="pull-left">' +
                            '       <div class="pull-left">' +
                            '           <span class="box-icon">' +
                            '               <img alt="" src="' + data.data.Cart[i].image + '">' +
                            '           </span>' +
                            '       </div>' +
                            '       <div class="box-cart-text">' +
                            '           <p class="font-line-3">' + data.data.Cart[i].name + '</p>' +
                            '       </div>' +
                            '   </div>' +
                            '   <div class="pull-right box-cart-price">' +
                            '       <p>¥' + data.data.Cart[i].price + '×' + data.data.Cart[i].numb + '</p>' +
                            '       <p style="float: right;">' +
                            '   </div>' +
                            '</div>';
                    };

                    $('.shopping').text(data.number);
                    $('#CartList').html(html);
                };
            })
            .fail(function(data) {
                console.log(data);
            })
            .always(function() {
                console.log("complete");
            });
    }
    /* 鼠标移入事件 */
    $('.cart').mouseover(function(event) {
        event.preventDefault();
        /* Act on the event */
        $('.box-cart').removeClass('box-cart-dis');
    });

    /* 右上角的购物车，获取购物车商品 */
    $('.btn-cart').mouseover(function(event) {
        event.preventDefault();
        /* Act on the event */
        posCart();
    });

    /* 鼠标移出事件 */
    $('.cart').mouseout(function(event) {
        event.preventDefault();
        /* Act on the event */
        $('.box-cart').addClass('box-cart-dis');
    });
    //posCart();
});


