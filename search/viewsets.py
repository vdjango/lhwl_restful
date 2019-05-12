import json

from django.core.paginator import InvalidPage, Paginator
from django.http import HttpResponse
from haystack.forms import ModelSearchForm
from haystack.query import EmptySearchQuerySet
from rest_framework.response import Response

from lhwill import settings

RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)

class RestSearchView(object):

    form = None
    query = ''
    request = None
    load_all = True
    object_list = []
    extra_context = {}
    searchqueryset = None
    form_class = ModelSearchForm
    results = EmptySearchQuerySet()
    results_per_page = RESULTS_PER_PAGE
    page = None

    def list(self, request, *args, **kwargs):
        if self.get_query_isValid():
            return self.restful_response(self.get_context_response())
        return self.restful_response({
            'detail': '请求方法未包含 “?q=foo” 查询参数'
        }, status=405)

    def restful_response(self, *args, **kwargs):
        return Response(*args, **kwargs)

    def get_context_response(self):
        """
        Generates the actual response to the search.

        Relies on internal, overridable methods to construct the response.
        """
        self.form = self.build_form()
        self.query = self.get_query()
        self.results = self.get_results()

        return self.get_context()

    def build_form(self, form_kwargs=None):
        """
        Instantiates the form the class should use to process the search query.
        """
        data = None
        kwargs = {
            'load_all': self.load_all,
        }
        if form_kwargs:
            kwargs.update(form_kwargs)

        if len(self.request.GET):
            data = self.request.GET

        if self.searchqueryset is not None:
            kwargs['searchqueryset'] = self.searchqueryset

        return self.form_class(data, **kwargs)

    def get_query_isValid(self):
        '''
        验证是否包含请求参数
        :return:
        '''
        if len(self.request.GET):
            return True
        return False

    def get_query(self):
        """
        Returns the query provided by the user.

        Returns an empty string if the query is invalid.
        """
        if self.form.is_valid():
            return self.form.cleaned_data['q']

        return ''

    def get_results(self):
        """
        Fetches the results via the form.

        Returns an empty list if there's no query to search with.
        """
        return self.form.search()

    def build_page(self):
        """
        Paginates the results appropriately.

        In case someone does not want to use Django's built-in pagination, it
        should be a simple matter to override this method to do what they would
        like.
        """
        try:
            page_no = int(self.request.GET.get('page', 1))
        except (TypeError, ValueError):
            raise self.restful_response("Not a valid number for page.", status=405)

        if page_no < 1:
            raise self.restful_response("Pages should be 1 or greater.", status=405)

        start_offset = (page_no - 1) * self.results_per_page
        self.results[start_offset:start_offset + self.results_per_page]

        paginator = Paginator(self.results, self.results_per_page)

        try:
            page = paginator.page(page_no)
        except InvalidPage:
            raise HttpResponse("No such page!")

        return (paginator, page)

    def get_context_data(self):
        """
        Allows the addition of more context variables as needed.

        Must return a dictionary.
        """
        return {}

    def get_request_query(self, page, **kwargs):
        '''
        组合query路径
        :param page:
        :param kwargs:
        :return:
        '''
        index_query = ''
        index = 0
        for i, k in self.request.GET.items():
            kwargs.update({
                i: k
            })
            kwargs['page'] = page
            pass

        for item, k in kwargs.items():
            index_query += '{}={}'.format(item, k)
            if index < kwargs.__len__()-1:
                index_query += '&'
                pass
            index += 1
            pass

        index_query = '{}{}?{}'.format(self.request.get_host(), self.request.path, index_query)

        if self.request.is_secure():
            index_query = 'https://{}'.format(index_query)
        else:
            index_query = 'http://{}'.format(index_query)
            pass

        return index_query

    def get_next_page_number(self, page):
        if page.has_next():
            return self.get_request_query(page.next_page_number())
        return None

    def get_previous_page_number(self, page):
        if page.has_previous():
            return self.get_request_query(page.previous_page_number())
        return None

    def get_content_results(self):
        object_list = []
        for item in self.page.object_list:
            object_list.append(item.get_stored_fields())
            pass
        return object_list

    def get_context(self):
        (paginator, page) = self.build_page()
        self.page = page

        context = {
            'query': self.query,
            'count': paginator.count,
            'pages_size': page.paginator.num_pages,
            'index': page.number,
            'next': self.get_next_page_number(page),
            'previous': self.get_previous_page_number(page),
            'results': self.get_content_results(),
        }

        context.update(self.get_context_data())

        return context
