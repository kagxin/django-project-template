from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.schedule.views import *

router = DefaultRouter()
router.register('task', CreateScheduleTask, basename='task')


urlpatterns = [
    path('', include(router.urls)),
]
