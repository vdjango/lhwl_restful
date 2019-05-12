from django.shortcuts import render, _get_queryset


class HttpResponseError(object):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        self.template_name = 'defaule/error/index.html'
        self.args = args
        self.kwargs = kwargs
        pass

    def HttpResponse_or_404(self):

        try:
            page = self.kwargs['page']
        except KeyError:
            page = 'page not found'

        try:
            title = self.kwargs['title']
        except KeyError:
            title = '对不起，您查找的页面不存在！'

        try:
            text = self.kwargs['text']
        except KeyError:
            text = '当您看到这个页面,表示您的访问出错,这个错误是您打开的页面不存在,请确认您输入的地址是正确的,' \
                   '如果是在本站点击后出现这个页面,请联系站长进行处理,或者请通过下边的搜索重新查找资源!'

        context = {
            'code': 404,
            'page': page,
            'title': title,
            'content': text,
        }
        return render(self.request, template_name=self.template_name, context=context,
                      status=404)

    def HttpResponse_or_403(self, *args, **kwargs):
        text = '当您看到这个页面,表示您的访问出错,这个错误是您打开的页面访问被拒绝,请确认您输入的地址是正确的,' \
               '如果是在本站点击后出现这个页面,请联系站长进行处理,或者请通过下边的搜索重新查找资源!'

        context = {
            'code': 403,
            'page': 'prohibition of access',
            'title': '对不起，您查找的页面被禁止访问！',
            'content': text,
        }
        return render(self.request, template_name=self.template_name, context=context,
                      status=403)

    def ResponseError(self, **kwargs):
        try:
            code = kwargs['code']
        except KeyError:
            code = 404
            pass
        try:
            page = kwargs['page']
        except KeyError:
            page = ''
            pass
        try:
            title = kwargs['title']
        except KeyError:
            title = '您访问的页面不存在'
            pass
        try:
            content = kwargs['content']
        except KeyError:
            content = '呼啦啦，呼啦啦。不知道东西去哪里了'
            pass

        context = {
            'code': code,
            'page': page,
            'title': title,
            'content': content,
        }
        return render(self.request, template_name=self.template_name, context=context,
                      status=403)

    def render_to_response(self, context):
        return render(self.request, template_name=self.template_name, context=context,
                      status=404)

    pass


def get_object_or_404(request, klass, *args, **kwargs):
    """
    Use get() to return an object, or raise a Http404 exception if the object
    does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
    one object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except AttributeError:
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    except queryset.model.DoesNotExist:
        return HttpResponseError(request).HttpResponse_or_404()
