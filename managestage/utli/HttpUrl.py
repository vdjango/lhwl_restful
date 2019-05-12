'''
Url 地址相关模块
'''
from django.shortcuts import render, HttpResponsePermanentRedirect

def UrlSection(number, Jumpurl):
    '''
        1    2     3     4
    0-30 30-60 60-90 90-120
    :param number: 切片起始页面
    :param Jumpurl: 切片范围溢出跳转地址
    :return: 切片长度
    '''
    number = int(number)
    if number != 0:
        Front = ((number - 1) * 3) * 10
        After = (number * 3) * 10
        print('UrlSection:', Front, After)
        return Front, After
    else:
        return HttpResponsePermanentRedirect('{u}/{n}/'.format(
            u=Jumpurl,
            n=1
        ))
