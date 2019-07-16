from django.views import View
from django.http import JsonResponse
from apps.utils.view.viewsets import ModelViewSet
from apps.demo.serializers import *
# Create your views here.

class TestView(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse(data={'message': 'hello world.'})


class ArticleViewSet(ModelViewSet):

    lookup_field = 'pk'
    serializer_class = ArticleSerializer
