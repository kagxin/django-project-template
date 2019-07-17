from rest_framework.views import *
from apps.core.exceptions import CustomAPIException
from apps.utils.response import simple_response
from apps.core import response_code


##
# 重写异常handler， 满足现有response 格式，
# 方便编码
###

def custom_exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}

        set_rollback()
        if exc.status_code == 400:
            code, message = response_code.ERR_PARAM_ERROR
        elif exc.status_code == 401:
            code, message = response_code.ERR_AUTH_ERROR
        elif exc.status_code == 403:
            code, message = response_code.ERR_PERMISSION_ERROR
        elif exc.status_code == 500:
            code, message = response_code.ERR_SERVER_ERROR
        elif exc.status_code == 405:
            code, message = response_code.ERR_METHOD_NOT_ALLOWED
        else:
            code, message = response_code.ERR_UNKNOWN_ERROR
        return simple_response(code=code,  data=data, message=message, headers=headers)

    elif isinstance(exc, CustomAPIException):  # 捕获自定义的异常
        set_rollback()
        return simple_response(code=exc.get_code(), message=exc.get_message(), data=exc.get_data())

    return None
