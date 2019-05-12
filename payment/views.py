import json
import time

from django.http import HttpResponse
from django.shortcuts import render

from alipay import AliPay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

notify_url = "http://www.lhwill.com/payment/aliapy_back_url/"  # 支付成功回掉的地址，在支付宝中设置




def aliplay_text(request):

    pass



@csrf_exempt
def ali():
    # 设置自己的私钥，将自己的公钥放在支付宝上
    merchant_private_key_path = settings.BASE_DIR + '/keys/pri/app_private_key.pem'  # 设置公钥和私钥的地址，文件上下两行begin和end是必须的，公钥就放在第二行。
    # 设置支付宝公钥，我用的是sha1加密方式的pem文件
    alipay_public_key_path = settings.BASE_DIR + '/keys/pub/pub.pem'
    app_private_key_string = open(merchant_private_key_path).read()
    alipay_public_key_string = open(alipay_public_key_path).read()
    app_id = "2018051660132699"  # 复制来自支付宝生成的id

    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,  # 默认回调url
        app_private_key_string=app_private_key_string,
        alipay_public_key_string=alipay_public_key_string,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False  # 默认False
    )
    return alipay


# 充值生成订单

@csrf_exempt
def recharge(request):
    alipay = ali()
    ret = {
        'code': 200,
        'msg': '请求成功!',
        'order_string': ''
    }

    user_id = request.GET.get('user_id')
    money = request.GET.get('money')

    try:
        # 生成订单
        order_string = alipay.api_alipay_trade_app_pay(
            out_trade_no="LB" + str(int(round(time.time()))),  # 商户订单号
            total_amount=str(money),
            subject="liuhuabi",  # 商品简单描述
            return_url=None
        )

        ret['code'] = 200


        ret['order_string'] = order_string
        ret['msg'] = "请求成功!"

        ret['url'] = settings.ALIPAY_URL + "?" + order_string

    except Exception as e:
        ret['code'] = 1010
        ret['msg'] = str(e)
        print(str(e))
        return HttpResponse(json.dumps(ret))

    print('生成订单', ret)

    return HttpResponse(json.dumps(ret))
# 返回订单的生成的订单码


@csrf_exempt
def aliapy_back_url(request):
    alipay = ali()
    if request.method == "POST":
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib import parse_qs

        # request.body                  => 字节类型
        # request.body.decode('utf-8')  => 字符串类型
        """ 
        {"k1":["v1"],"k2":["v1"]} 
        k1=[v1]&k2=[v2] 
        """
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)
        # {k1:[v1,],k2:[v2,]}

        # {k1:v1}
        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        print(post_dict)
        """ 
        {'gmt_create': '2017-11-24 14:53:41', 'charset': 'utf-8', 'gmt_payment': '2017-11-24 14:53:48', 'notify_time': '2017-11-24 14:57:05', 'subject': '充气式韩红', 'sign': 'YwkPI9BObXZyhq4LM8//MixPdsVDcZu4BGPjB0qnq2zQj0SutGVU0guneuONfBoTsj4XUMRlQsPTHvETerjvrudGdsFoA9ZxIp/FsZDNgqn9i20IPaNTXOtQGhy5QUetMO11Lo10lnK15VYhraHkQTohho2R4q2U6xR/N4SB1OovKlUQ5arbiknUxR+3cXmRi090db9aWSq4+wLuqhpVOhnDTY83yKD9Ky8KDC9dQDgh4p0Ut6c+PpD2sbabooJBrDnOHqmE02TIRiipULVrRcAAtB72NBgVBebd4VTtxSZTxGvlnS/VCRbpN8lSr5p1Ou72I2nFhfrCuqmGRILwqw==', 'buyer_id': '2088102174924590', 'invoice_amount': '666.00', 'version': '1.0', 'notify_id': '11aab5323df78d1b3dba3e5aaf7636dkjy', 'fund_bill_list': '[{"amount":"666.00","fundChannel":"ALIPAYACCOUNT"}]', 'notify_type': 'trade_status_sync', 'out_trade_no': 'x21511506412.4733646', 'total_amount': '666.00', 'trade_status': 'TRADE_SUCCESS', 'trade_no': '2017112421001004590200343962', 'auth_app_id': '2016082500309412', 'receipt_amount': '666.00', 'point_amount': '0.00', 'app_id': '2016082500309412', 'buyer_pay_amount': '666.00', 'sign_type': 'RSA2', 'seller_id': '2088102172939262'} 
        {'stade_status': "trade_success",'order':'x2123123123123'} 
        """
        sign = post_dict.pop('sign', None)

        status = alipay.verify(post_dict, sign)
        if status:
            print(post_dict['stade_status'])
            print(post_dict['out_trade_no'])

            return HttpResponse('POST返回')
    else:
        # QueryDict = {'k':[1],'k1':[11,22,3]}
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        print('GET验证', status)
        return HttpResponse('支付成功')
