from rest_framework.response import Response
from rest_framework import status as http_status
from apps.core import response_code


def simple_response(code=response_code.SUCCESS[0], message=response_code.SUCCESS[1], data=None,
                    status=http_status.HTTP_200_OK, headers=None):
    if data is None:
        data = dict()

    response_data = dict(
        code=code,
        message=message,
        data=data
    )
    return Response(data=response_data, status=status, headers=headers)
