from rest_framework import serializers
from apps.demo.models import *


class ReporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reporter
        fields = ['__all__']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['__all__']
