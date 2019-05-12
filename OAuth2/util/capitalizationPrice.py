# -*- coding: utf-8 -*-
#

'''
转换数字为大写金额
'''


def price(num):
    '''
    转换数字为大写金额
    :param num:
    :return:
    '''
    cdata = str(num).split('.')
    ckj = "0"
    num = cdata[0]
    if len(cdata) > 1:
        ckj = cdata[1]

    dic_num = {
        "0": u"零",
        "1": u"壹",
        "2": u"贰",
        "3": u"叁",
        "4": u"肆",
        "5": u"伍",
        "6": u"陆",
        "7": u"柒",
        "8": u"捌",
        "9": u"玖"
    }
    dic_unit = {
        0: "",
        1: u"拾",
        2: u"佰",
        3: u"仟",
        4: u"万",
        5: u"拾",
        6: u"佰",
        7: u"仟",
        8: u"亿"
    }

    # num = "12345"
    numList = list(str(num))
    s = ""
    a = ""
    x = 0
    index = len(str(num)) - 1
    for i in numList:
        if i == "0":
            if index == 4:
                a = "万"
            x = x + 1
        else:
            if x > 0:
                s += a + u"零" + dic_num[i] + dic_unit[index]
            else:
                s += dic_num[i] + dic_unit[index]
            x = 0
        index -= 1
    s = s + "元"
    lenkj = len(ckj)
    if lenkj == 1:  # 若小数只有1位
        if int(ckj[0]) == 0:
            s = s + u'整'
        else:
            # print('小数有', dic_num[ckj[0]], '位')
            # s = s+dic_num[int(ckj[0])]+u'角整'
            s = s + dic_num[ckj[0]] + u'角整'
    else:  # 若小数有两位的四种情况
        if int(ckj[0]) == 0 and int(ckj[1]) != 0:
            s = s + u'零' + dic_num[(ckj[1])] + u'分'
        elif int(ckj[0]) == 0 and (ckj[1]) == 0:
            s = s + u'整'
        elif int(ckj[0]) != 0 and (ckj[1]) != 0:
            s = s + dic_num[(ckj[0])] + u'角' + dic_num[(ckj[1])] + u'分'
        else:
            s = s + dic_num[(ckj[0])] + u'角整'

    return s
