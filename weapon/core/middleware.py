import json

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler as origin_exception_handler


def parse_context(context):
    return str(context)


def drf_exception_handler(exc, context):
    response = origin_exception_handler(exc, context)
    if response is None:
        return None

    # Update the structure of the response data.
    if response is not None:
        customized_response = {}
        customized_response['details'] = []
        customized_response["code"] = 999999

        for key, value in response.data.items():
            error = {'field': key, 'message': value}
            customized_response['details'].append(error)

        response.data = customized_response

    return response

# class DRFResponseMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         # One-time configuration and initialization.

#     def __call__(self, request):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.

#         response = self.get_response(request)

#         # Code to be executed for each request/response after
#         # the view is called.

#         if isinstance(response, Response):
#             if hasattr(response, 'data') \
#                 and isinstance(response.data, dict) \
#                 and response.status_code == status.HTTP_200_OK:

#                 data = response.data.copy()

#                 data = json.loads(str(data))

#                 response.data = {
#                     'data': data,
#                     'code': 0
#                 }
#                 response.content = bytes(json.dumps(response.data), encoding='utf8')
#                 response._headers['content-length'] = ('Content-Length', str(len(response.content)))

#         return response
