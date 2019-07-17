from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.core.cache import caches
from apps.core.exceptions import CustomAPIException
from apps.core import response_code


class CheckTokenChangeAuthentication(JSONWebTokenAuthentication):

    def authenticate(self, request):
        auth = super().authenticate(request)
        if not auth:
            return auth
        user, jwt_value = auth
        cache_key = 'user:jwt:{user_id}'.format(user_id=user.id)
        l_jwt_value = caches['token'].get(cache_key)
        if l_jwt_value != jwt_value.decode('utf8'):
            code, message = response_code.ERR_TOKEN_CHANGED_ERROR
            raise CustomAPIException(code=code, message=message)

        return user, jwt_value
