# -*- coding: utf-8 -*-

from http import HTTPStatus

from django.http import JsonResponse

class JsonErrorMiddleware:
    '''
    将 Http404 等页面转化为 JsonResponse
    '''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        status_code = response.status_code
        if status_code >= 300:
            return self.handleException(status_code, request, response)

        return response

    def handleException(self, status_code, request, response):
        try:
            status_text = HTTPStatus(status_code).phrase
        except KeyError:
            status_text = 'Unsupported Operation'

        return JsonResponse({
            'status_code': status_code,
            'status_text': status_text,
            'data': {
                'request_url': request.get_full_path(),
                'request_method': request.method,
            },
        })
