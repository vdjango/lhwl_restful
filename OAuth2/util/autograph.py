import base64
import json

import requests
from Cryptodome.Hash import SHA, MD5
from Cryptodome.PublicKey import RSA
from Cryptodome.Signature import PKCS1_v1_5, pkcs1_15

from home import models
from home.models import Order, Suborderlist, Goodslist, Logistics, Acceptance
from lhwill import settings
from lhwill.util import log
from managestage.utli.datetimenow import datetimenowS, datetimenow


class AutoRsaGraph(object):
    '''
    订单接口
    '''

    def __init__(self, usercode, orderid):
        self.ApiUrl = 'http://mall-api.zycg.gov.cn'
        self.priKey = '''-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCsAiCNz0SMIhMoQtxmgphUqxYSW+wXz9Ub9EuRKXrFVPUc0Dm9
6Mn/zwNkmsiqfjw1UOVhnm6lKERSXUZ/1y+Xfhn16zsj6uBVtRa+G4g+S/sDNBvM
GjHxqba7AtihEVslmrNfEmb0T6T0QbV80gqnb9idCCFpsMroGJtDCMXFrQIDAQAB
AoGAS0avCoCfxhgPfDoujGow0jUBds1luFILOK2j+IZHpV512sNB0duzs1DcckXO
9dZC8S5TBHK6h2rk44rQlJgOyi0GvIpaIKKPDii7PcOIm8ortmuKvDb/9iNonSsX
QqAVr/aSHstE2TWgx5r1rVQC3UDqSNAKJJZvyWMq13o16wECQQDT6jmY7rnDxiex
lB7HQiLhe+6PAuR1bqyu6rAsuNJ1yCv1sMJOAh/kLU83gn5Bu46urOoZtF1nBMmZ
vhaL8IpBAkEAz8qg3XH+BRR6i4/q19z3snFLQmmfbXUGYURf2RxNQJvbG3IMHyCk
O/bqR4RHX7388+itgrE8O3Qg6jQGUhDobQJASc7opLVxChj4NkdquOf2EicCHdla
DPSxPHMNTWZKFy/S783SvyzKQsTtNF5E70wOFBSxrKY/aeQm+19TpwXugQJBAIfY
I7TCGlx91+O3scNvzWuWT6paXQT1FbevOK46p3KOsf7OX4hWEai2MtGQdAzuqxlW
S2D+t67yq7YRTvSF4z0CQALqqK/SArm3qsAc4XcAhoIPzgELzcqBF2Xsqlp0pEx2
IivDCEwCkCL6CXwa5qoEHXrskarZuhDe3yZhRnuKj80=
-----END RSA PRIVATE KEY-----'''
        self.time = datetimenowS()
        self.username = 'mall_lhwl'
        self.passwd = '6i2hvvpvv2wmrvt9'
        self.passwd = '{}{}'.format(self.passwd, self.time).encode(encoding="utf-8")
        self.datatime = str(datetimenow()).split('.')[0]
        self.headers = {'Content-Type': 'application/json;charset=utf-8'}
        self.usercode = usercode
        self.orderid = orderid  # 订单ID

        '''
        订单基本信息
        :return:
        '''
        try:
            self.orderModel = Order.objects.get(orderid=self.orderid)
            self.total = float(self.orderModel.total)  # '总订单 成交总价'
            self.province = self.orderModel.province  # '北京'
            self.city = self.orderModel.city  # '北京'
            self.deliveryaddress = self.orderModel.deliveryaddress  # '详细地址'
            self.name = self.orderModel.linkman  # '名字'
            self.phone = self.orderModel.linkmobile  # '电话号'
            self.remark = self.orderModel.remark  # '订单备注'
            self.paymethod = int(self.orderModel.paymethod)  # 付款方式
            self.ispaid = int(self.orderModel.ispaid)  # 是否完成支付、结清账期
            self.ordispaid = int(self.orderModel.ordispaid)
            self.suborder = Suborderlist.objects.get(key=self.orderModel)
            self.subtotal = float(self.suborder.total)  # '子订单总金额 不可大于总订单金额'
            '''
            子订单基本信息
            '''
            self.good = Goodslist.objects.filter(key=self.suborder)
            '''物流订单信息'''
            self.istics = Logistics.objects.filter(key=self.orderModel)
        except:
            log.i(globals(), '没有获取到Order订单信息，跳过')
            pass

    def sign(self):
        key = RSA.importKey(self.priKey)
        signer = PKCS1_v1_5.new(key)
        h = MD5.new(self.passwd)
        signature = signer.sign(h)
        code = base64.urlsafe_b64encode(signature)
        return code.decode()

    def order_create(self):
        '''
        创建订单
        :return:
        '''
        if not self.usercode or self.usercode == '':
            log.i(globals(), '非国采用户，跳过创建订单')
            return False

        url = settings.HTTP_HOST
        goodslist = []
        for i in self.good:
            goodslist.append(
                {
                    'goodsname': i.goodsname,
                    'goodsid': i.goodsid,
                    'spu': i.spu,
                    'sku': i.sku,
                    'model': i.model,
                    'goodsclassguid': int(i.goodsclassguid),
                    'goodsclassname': i.goodsclassname,
                    'goodsbrandname': i.goodsbrandname,
                    'qty': int(i.qty),
                    'total': float(i.total),
                    'price': float(i.price),
                    'originalprice': float(i.originalprice),
                    'imgurl': i.get_image_url(),
                    'goodsurl': '{}{}'.format(url, i.goodsurl)
                }
            )
        pass

        data = {
            'user': {
                'username': self.username,
                'code': self.sign()
            },
            'param': {
                'orderid': self.orderid,
                'province': self.province,
                'city': self.city,
                'total': float(self.total),
                'linkman': self.name,
                'linkmobile': self.phone,
                'deliveryaddress': self.deliveryaddress,
                'paymethod': self.paymethod,
                'ispaid': self.ispaid,
                'remark': self.remark,
                'usercode': self.usercode,
                'createtime': self.datatime,
                'suborderlist': [
                    {
                        'suborderid': self.orderid,  # 后期可能需要修改
                        'total': float(self.subtotal),
                        'goodslist': goodslist
                    }
                ]
            }
        }

        log.i(globals(), 'DATE ', data)

        html = requests.post(url='{}/api/order_create'.format(self.ApiUrl), data=json.dumps(data), headers=self.headers)

        dicts = json.loads(html.text)

        if dicts['returnmessage']['code'] == 1:
            log.i(globals(), '国采用户，创建订单', json.loads(html.text))

            Acceptance(
                orderid=self.orderid,
                usercode=self.usercode,
                time=datetimenow()
            ).save()
        else:
            # 验收单创建失败
            # 后续处理
            models.Error_Order(
                info=1,
                mess='[orderid={}],[total={}],[return={}]'.format(self.orderid, self.total, dicts),
                key=self.orderModel,
                time=datetimenow()
            ).save()
            log.i(globals(), '【失败】国采用户，创建订单 ', json.loads(html.text))
            pass

        return dicts
        pass

    '''更新订单-如果数据库ispaid为1 则申请生成验收单'''

    def order_knot(self):
        '''
        更新订单-如果数据库ispaid为1 则申请生成验收单
        0 没付款
        1 款结了
        :return:
        '''
        if not self.usercode or self.usercode == '':
            log.i(globals(), '非国采用户，跳过更新订单-如果数据库ispaid为1 则申请生成验收单')
            return False

        if self.ispaid == 1:
            # 款结了 申请生成验收单
            data = {
                'user': {
                    'username': self.username,
                    'code': self.sign()
                },
                'param': {
                    'orderid': self.orderid,
                    'type': 1,  # 已验收完成（申请生成验收单）
                    'paymethod': self.paymethod,
                    'ispaid': self.ispaid
                }
            }
            html = requests.post(url='{}/api/order_update'.format(self.ApiUrl), data=json.dumps(data),
                                 headers=self.headers)
            dicts = json.loads(html.text)

            if dicts['returnmessage']['code'] == 1:
                log.i(globals(), '国采用户，款结了 申请生成验收单', dicts, dicts['returnmessage']['ysd_code'])
                acc = Acceptance.objects.get(orderid=self.orderid)
                acc.state = 0
                acc.ysd_code = dicts['returnmessage']['ysd_code']
                acc.save()
            else:
                # 验收单创建失败
                # 后续处理
                models.Error_Order(
                    info=1,
                    mess='[orderid={}],[total={}],[return={}]'.format(self.orderid, self.total, dicts),
                    key=self.orderModel,
                    time=datetimenow()
                ).save()
                log.i(globals(), '【失败】国采用户，款结了 申请生成验收单 ', json.loads(html.text))
                pass
            return json.loads(html.text)
            pass
        else:
            # 没付款
            log.i(globals(), '国采用户，没付款,不更新订单信息', self.ispaid)
            pass
        return False
        pass

    '''更新订单-更新支付信息 以完成支付'''

    def order_PaymentCompletion(self):
        '''
        更新订单-更新支付信息 以完成支付
        0 没付款
        1 款结了
        :return:
        '''
        if not self.usercode or self.usercode == '':
            log.i(globals(), '非国采用户，跳过更新订单-更新支付信息 以完成支付')
            return False

        if self.ispaid == 0:
            # 没付款
            data = {
                'user': {
                    'username': self.username,
                    'code': self.sign()
                },
                'param': {
                    'orderid': self.orderid,
                    'type': 2,  # 更新支付信息，需附带paymethod、ispaid参数
                    'paymethod': self.paymethod,
                    'ispaid': 1  # 款结了
                }
            }
            html = requests.post(url='{}/api/order_update'.format(self.ApiUrl), data=json.dumps(data),
                                 headers=self.headers)

            if html:
                self.orderModel.ispaid = 1
                self.orderModel.save()
                pass

            dicts = json.loads(html.text)

            if dicts['returnmessage']['code'] == 1:
                log.i(globals(), '国采用户，更新订单-更新支付信息 以完成支付', json.loads(html.text))
            else:
                # 验收单创建失败
                # 后续处理
                models.Error_Order(
                    info=1,
                    mess='[orderid={}],[total={}],[return={}]'.format(self.orderid, self.total, dicts),
                    key=self.orderModel,
                    time=datetimenow()
                ).save()
                log.i(globals(), '【失败】国采用户，更新订单-更新支付信息 以完成支付 ', json.loads(html.text))
                pass
            return dicts
            pass
        else:
            # 以付款
            log.i(globals(), '国采用户，以付款,不更新订单信息', self.ispaid)
            pass
        return False
        pass

    def order_update(self, ispaid=None):
        '''
        更新订单 创建验收单
        0 没付款
        1 款结了
        :return:
        '''
        if not self.usercode or self.usercode == '':
            log.i(globals(), '非国采用户，跳过更新订单 创建验收单')
            return False

        if ispaid:
            self.ispaid = ispaid

        data = {
            'user': {
                'username': self.username,
                'code': self.sign()
            },
            'param': {
                'orderid': self.orderid,
                'type': 1,  # '请求类型'
                'paymethod': self.paymethod,
                'ispaid': self.ispaid
            }
        }

        html = requests.post(url='{}/api/order_update'.format(self.ApiUrl), data=json.dumps(data), headers=self.headers)
        dicts = json.loads(html.text)

        if dicts['returnmessage']['code'] == 1:
            log.i(globals(), '国采用户，更新订单 创建验收单', dicts, dicts['returnmessage'])
            acc = Acceptance.objects.get(orderid=self.orderid)
            acc.state = 0
            acc.ysd_code = dicts['returnmessage']['ysd_code']
            acc.save()
        else:
            # 验收单创建失败
            # 后续处理
            models.Error_Order(
                info=1,
                mess='[orderid={}],[total={}],[return={}]'.format(self.orderid, self.total, dicts),
                key=self.orderModel,
                time=datetimenow()
            ).save()
            log.i(globals(), '【失败】国采用户，更新订单 创建验收单 ', dicts)
            pass
        return dicts
        pass

    def order_delete(self, stype=0):
        '''
        取消整个订单（生成验收单之前）
        根据验收单是否生成 而采取 取消验收单还是作废验收单操作
        :return:
        '''
        if not self.usercode or self.usercode == '':
            log.i(globals(), '非国采用户，跳过取消整个订单（生成验收单之前）')
            return False

        if self.ordispaid == 0:
            data = {
                'user': {
                    'username': self.username,
                    'code': self.sign()
                },
                'param': {
                    'orderid': self.orderid,
                    'type': stype  # '请求类型'
                }
            }
            html = requests.post(url='{}/api/order_update'.format(self.ApiUrl), data=json.dumps(data),
                                 headers=self.headers)
            dicts = json.loads(html.text)
            log.i(globals(), '国采用户，取消整个订单（生成验收单之前）', json.loads(html.text))
        elif self.ordispaid == 2:
            data = {
                'user': {
                    'username': self.username,
                    'code': self.sign()
                },
                'param': {
                    'orderid': self.orderid,
                    'type': 7  # 作废整个订单（退货，生成验收单之后）
                }
            }
            html = requests.post(url='{}/api/order_update'.format(self.ApiUrl), data=json.dumps(data),
                                 headers=self.headers)
            dicts = json.loads(html.text)

        if dicts['returnmessage']['code'] == 1:
            log.i(globals(), '国采用户，取消整个订单（生成验收单之前）', json.loads(html.text))

        else:
            # 验收单创建失败
            # 后续处理
            models.Error_Order(
                info=1,
                mess='[orderid={}],[total={}],[return={}]'.format(self.orderid, self.total, json.loads(html.text)),
                key=self.orderModel,
                time=datetimenow()
            ).save()
            log.i(globals(), '【失败】国采用户，取消整个订单（生成验收单之前） ', json.loads(html.text))
            pass
        return dicts
        pass

    def order_delete_on(self):
        '''
        作废整个订单（生成验收单之后）
        :return:
        '''
        # if not self.usercode or self.usercode == '':
        # 	log.i(globals(), '非国采用户，跳过作废整个订单（生成验收单之后）')
        # 	return False

        data = {
            'user': {
                'username': self.username,
                'code': self.sign()
            },
            'param': {
                'orderid': self.orderid,
                'type': 7  # 作废整个订单（退货，生成验收单之后）
            }
        }
        html = requests.post(url='{}/api/order_update'.format(self.ApiUrl), data=json.dumps(data),
                             headers=self.headers)
        dicts = json.loads(html.text)

        if dicts['returnmessage']['code'] == 1:
            log.i(globals(), '国采用户，作废整个订单（生成验收单之前）', json.loads(html.text))
            acc = Acceptance.objects.get(orderid=self.orderid)
            acc.state = -1
            acc.save()
            # 订单中的验收单状态
            self.orderModel.ordispaid = -1
            self.orderModel.save()
        else:
            # 验收单创建失败
            # 后续处理
            models.Error_Order(
                info=1,
                mess='[orderid={}],[total={}],[return={}]'.format(self.orderid, self.total, json.loads(html.text)),
                key=self.orderModel,
                time=datetimenow()
            ).save()
            log.i(globals(), '【失败】国采用户，作废整个订单（生成验收单之前） ', json.loads(html.text))
            return False
            pass
        return dicts
        pass

    def order_logistics(self):
        '''
        物流推送接口， 全量推送
        只推送数据库里面的物流信息
        :return:
        '''
        if not self.usercode or self.usercode == '':
            log.i(globals(), '非国采用户，跳过物流推送接口， 全量推送')
            return False

        logisticslist = []
        for i in self.istics:
            logisticslist.append({
                'time': str(i.time.astimezone()).split('+')[0],
                'info': i.info,
                'username': i.username
            })
            pass

        data = {
            'user': {
                'username': self.username,
                'code': self.sign()
            },
            'param': {
                'orderid': self.orderid,
                'suborderid': self.orderid,  # '子订单号（卖场）',
                'logisticslist': logisticslist
            }
        }

        html = requests.post(url='{}/api/order_logistics'.format(self.ApiUrl), data=json.dumps(data),
                             headers=self.headers)
        dicts = json.loads(html.text)

        if dicts['returnmessage']['code'] == 1:
            log.i(globals(), '国采用户，物流推送接口， 全量推送', json.loads(html.text))
        else:
            # 验收单创建失败
            # 后续处理
            models.Error_Order(
                info=1,
                mess='[orderid={}],[total={}],[return={}]'.format(self.orderid, self.total, json.loads(html.text)),
                key=self.orderModel,
                time=datetimenow()
            ).save()
            log.i(globals(), '【失败】国采用户，物流推送接口， 全量推送 ', json.loads(html.text))
            pass
        return json.loads(html.text)
        pass
