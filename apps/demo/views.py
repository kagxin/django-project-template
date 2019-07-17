from django.views import View
from django.http import JsonResponse
from apps.utils.view.viewsets import ModelViewSet
from apps.demo.serializers import *
from apps.utils.pagination import DefaultResultsSetPagination
from apps.demo import filters
import logging

# Create your views here.

class TestView(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse(data={'message': 'hello world.'})


class ArticleViewSet(ModelViewSet):
    lookup_field = 'pk'
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    pagination_class = DefaultResultsSetPagination
    filter_class = filters.ProductFilter

    def list(self, request, *args, **kwargs):
        log = logging.getLogger('view')
        log.info(f'{request.user}')
        return super().list(request, *args, **kwargs)


class ReporterViewSet(ModelViewSet):
    lookup_field = 'pk'
    serializer_class = ReporterSerializer
    queryset = Reporter.objects.all()
    pagination_class = DefaultResultsSetPagination
