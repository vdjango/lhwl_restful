from account.models import User
from shopping import models
from .cart import Cart


def template_defaule(request):
    '''
    上下文处理器
    :param request:
    :return:
    '''
    Cart = []
    try:
        Cart = models.Cart.objects.filter(user=request.user.username)
        number = len(Cart)
    except:
        number = 0

    context = {
        'cart': {
            'Cart': Cart,
            'number': number
        }
    }
    return context
