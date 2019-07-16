# from django.contrib.auth import get_user_model
from rest_framework_jwt.utils import jwt_payload_handler as _jwt_payload_handler
from rest_framework_jwt.utils import jwt_response_payload_handler as _jwt_response_payload_handler


def jwt_payload_handler(user):
    return _jwt_payload_handler(user)


def jwt_response_payload_handler(token, user=None, request=None):
    return _jwt_response_payload_handler(token, user=user, request=request)
