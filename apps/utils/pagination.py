from rest_framework.pagination import PageNumberPagination


class DefaultResultsSetPagination(PageNumberPagination):
    page_size = 20  #默认单页面20个
    page_size_query_param = 'page_size' #可通过该参数自己设置每页多少个
    page_query_param = "page_index"  #t通过该参数选择多少页
    max_page_size = 100     #通过url修改参数  最大单页面100个