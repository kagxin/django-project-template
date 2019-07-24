from rest_framework.pagination import PageNumberPagination
from apps.utils.response import simple_response
from django.core.paginator import InvalidPage


class DefaultResultsSetPagination(PageNumberPagination):
    page_size = 20  #默认单页面20个
    page_size_query_param = 'page_size' #可通过该参数自己设置每页多少个
    page_query_param = "page_index"  #t通过该参数选择多少页
    max_page_size = 100     #通过url修改参数  最大单页面100个

    def get_paginated_response(self, data):
        reponse_data = super().get_paginated_response(data).data
        return simple_response(data=reponse_data)

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage:  # 无效的页码返回最后一页数据
            self.page = paginator.page(paginator.num_pages)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)