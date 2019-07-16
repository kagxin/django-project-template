from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.demo.views import *

router = DefaultRouter()
router.register('article', ArticleViewSet, basename='article')
router.register('reporter', ReporterViewSet, basename='article')


urlpatterns = [
    path('', include(router.urls)),
    path('demo/', TestView.as_view(), name='demo')
]
