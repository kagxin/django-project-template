from django.views import View
from django.http import JsonResponse
from apps.utils.view.viewsets import ModelViewSet
from apps.demo.serializers import *
from apps.utils.pagination import DefaultResultsSetPagination


# Create your views here.

class TestView(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse(data={'message': 'hello world.'})


class ArticleViewSet(ModelViewSet):
    lookup_field = 'pk'
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    pagination_class = DefaultResultsSetPagination

    def dispatch(self, request, *args, **kwargs):
        # print(request)
        # print(self.http_method_names)
        print(self.allowed_methods)
        # print(self.request.method.lower())
        # print(getattr(self, 'get'))
        # print(getattr(self, 'delete'))

        return super().dispatch(request, *args, **kwargs)


class ReporterViewSet(ModelViewSet):
    lookup_field = 'pk'
    serializer_class = ReporterSerializer
    queryset = Reporter.objects.all()
    pagination_class = DefaultResultsSetPagination
