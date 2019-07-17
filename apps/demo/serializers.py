from rest_framework import serializers
from apps.core.exceptions import CustomAPIException
from apps.core import response_code
from apps.demo.models import *


class ReporterSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=True)

    def validate_full_name(self, value):
        if 'admin' in value.lower():
            code, message = response_code.ERR_ADMIN_IN_FULLNAME
            raise CustomAPIException(code=code, message=message)
        return value

    class Meta:
        model = Reporter
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
