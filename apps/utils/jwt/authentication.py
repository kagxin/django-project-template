from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.core.cache import caches
from apps.core.exceptions import CustomAPIException
from apps.core import response_code


class SingleUserLoginAuthentication(JSONWebTokenAuthentication):

    def authenticate(self, request):
        user, jwt_value = super().authenticate(request)
        print(user, jwt_value)
        cache_key = f'jwt:token:{user.id}'
        l_jwt_value = caches['token'].get(cache_key)
        if l_jwt_value != jwt_value:
            code, message = response_code.ERR_LOGIN_OTHER_CLIENT_ERROR
            raise CustomAPIException(code=code, message=message)

        return user, jwt_value
