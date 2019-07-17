from rest_framework_jwt.views import ObtainJSONWebToken, RefreshJSONWebToken, VerifyJSONWebToken
from rest_framework_jwt.serializers import VerificationBaseSerializer
from rest_framework_jwt.settings import api_settings
from django.core.cache import caches
from apps.core import response_code
from apps.core.exceptions import CustomAPIException
from apps.utils.exception_handler import custom_exception_handler

jwt_decode_handle = api_settings.JWT_DECODE_HANDLER


class VerifyJSONWebTokenSerializer(VerificationBaseSerializer):
    """
    Check the veracity of an access token.
    """

    def validate(self, attrs):
        token = attrs['token']

        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)
        return {
            'token': token,
            'user': user
        }

    def to_representation(self, instance):
        return instance


class SaveTokenToCacheMixin:
    token_filed_name = 'token'
    user_id_filed_name = 'user_id'

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data.get(self.token_filed_name, '')
        if not token:
            """检查jwt_response_payload_handler 中是否有{}字段""".format(self.token_filed_name)
            raise RuntimeError('Check if there is a token field in response.')
        payload = jwt_decode_handle(token)
        user_id = payload.get('user_id')
        if not user_id:
            """检查jwt_response_payload_handler 中是否有{}字段""".format(self.user_id_filed_name)
            raise RuntimeError('Check if there is a user_id field in response.')

        cache_key = 'user:jwt:{user_id}'.format(user_id=payload[self.user_id_filed_name])
        caches['token'].set(cache_key, token, timeout=None)
        print(cache_key, token)
        return response


class ObtainJSONWebTokenChangeTokenChangeView(SaveTokenToCacheMixin, ObtainJSONWebToken):
    pass


class CheckTokenChangedAndSaveMixin(SaveTokenToCacheMixin):

    def get_exception_handler(self):
        return custom_exception_handler

    def post(self, request, *args, **kwargs):
        serializer = VerifyJSONWebTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.data)
        user = serializer.data.get('user')
        token = serializer.data.get('token')
        cache_key = 'user:jwt:{user_id}'.format(user_id=user.id)
        l_jwt_value = caches['token'].get(cache_key)
        if l_jwt_value != token:
            code, message = response_code.ERR_TOKEN_CHANGED_ERROR
            raise CustomAPIException(code=code, message=message)
        return super().post(request, *args, **kwargs)


class RefreshJSONWebTokenChangeTokenChangeView(CheckTokenChangedAndSaveMixin, RefreshJSONWebToken):
    pass


class VerifyJSONWebTokenChangeTokenChangeView(CheckTokenChangedAndSaveMixin, VerifyJSONWebToken):
    pass


obtain_jwt_check_token_change = ObtainJSONWebTokenChangeTokenChangeView.as_view()
refresh_jwt_check_token_change = RefreshJSONWebTokenChangeTokenChangeView.as_view()
verify_jwt_check_token_change = VerifyJSONWebTokenChangeTokenChangeView.as_view()