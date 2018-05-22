# -*- coding: utf-8 -*-

from http import HTTPStatus
import json

from django.http import JsonResponse

def _log(request, response):
    print('''
        General
            Request URL:        {}
            Request Method:     {}
            Status Code:        {}
            Remote Address:     {}
        ------------------------------------
        Request Headers
            Accept:             {}
            Accept-Encoding:    {}
            Accept-Language:    {}
            Connection:         {}
            Content-Length:     {}
            Content-Type:       {}
            Cookie:             {}
            Host:               {}
            Origin:             {}
            Referer:            {}
            User-Agent:         {}
        '''.format(
            # Request URL
            request.build_absolute_uri(),
            # Request Method
            request.method,
            # Status Code
            response.status_code,
            # Remote Address
            request.META.get('REMOTE_ADDR', ''),
            # ------------------------------------
            # Accept
            request.META.get('HTTP_ACCEPT', ''),
            # Accept-Encoding
            request.META.get('HTTP_ACCEPT_ENCODING', ''),
            # Accept-Language
            request.META.get('HTTP_ACCEPT_LANGUAGE', ''),
            # Connection
            request.META.get('HTTP_CONNECTION', ''),
            # Content-Length
            request.META.get('CONTENT_LENGTH', ''),
            # Content-Type
            request.META.get('CONTENT_TYPE', ''),
            # Cookie
            request.META.get('HTTP_COOKIE', ''),
            # Host
            request.META.get('HTTP_HOST', ''),
            # Origin
            request.META.get('HTTP_ORIGIN', ''),
            # Referer
            request.META.get('HTTP_REFERER', ''),
            # User-Agent
            request.META.get('HTTP_USER_AGENT', ''),
        ))

def _sync_status(response):
    response.status_code = json.loads(response.content).get('status_code', response.status_code)
    return response

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

        _log(request, response)

        # Code to be executed for each request/response after
        # the view is called.
        status_code = response.status_code
        if status_code >= 400:
            response = self.handleException(status_code, request, response)

        response = _sync_status(response)

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
