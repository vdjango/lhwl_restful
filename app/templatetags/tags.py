from django import template
from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()


@register.filter(is_safe=True)
def disc(v, k):
    print(v, k)
    return v
    pass


@stringfilter
@register.filter(is_safe=True)
def lens(d):
    value = ""
    try:
        for x in range(len(d)):
            value += str(x + 1)

    except KeyError:
        value = None

    print('len', value)
    return value


class SetVarNode(template.Node):
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""


def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])


len


@stringfilter
@register.filter(is_safe=True)
def section(k, v):
    '''
    字符串切片操作
    :param k: 字符串
    :param v: 切片长度
    :return:
    '''
    return k[:v]


@stringfilter
@register.filter(is_safe=True)
def spit(k, v):
    '''
    字符串切片操作
    :param k: 字符串
    :param v: 切片长度
    :return:
    '''
    nu = 0  # split——
    strings = ''
    len_spit = 0
    spit_auto = False

    nu = len(k) / v

    if nu >= len_spit:

        nu_str = str(nu).split('.')
        if int(nu_str[1]) != 0:
            nu = int(nu_str[0]) + 1
            spit_auto = True
        else:
            nu = int(nu_str[0])
            spit_auto = False
            pass
        pass
    # print('元数据', k, 'auto', spit_auto, nu_str)

    for i in range(nu):
        if i == (nu - 1):
            strings = str(strings) + str(k[len_spit:len(k)]) + ' '
            # print('spit_auto', strings, len_spit, len(k), v * i)
            return strings
            pass

        if i != 0:
            # print('range', str(k[len_spit:v * i]), v * i)
            strings = str(strings) + str(k[len_spit:v * i]) + ' '
            len_spit = v * i
        else:
            # print('range', str(k[len_spit:v * i]), v * i)
            strings = str(strings) + str(k[len_spit:v]) + ' '
            len_spit += v
        pass

    return strings


register.tag('set', set_var)
