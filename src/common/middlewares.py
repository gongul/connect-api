from django.http.response import Http404, HttpResponseRedirect
from django.db.utils import OperationalError
from django.urls.base import reverse
from rest_framework.exceptions import APIException, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler

from .errors import ErrorCollection


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, NotAuthenticated) and (context['request'].path == reverse('redoc') or context['request'].path == reverse('swagger-ui')):
        return HttpResponseRedirect(reverse('doc-login'))

    error_list = exception_format(exc)

    if not response:
        response = Response(status=500)

    response.data = {'status_code': response.status_code, 'errors': error_list}

    return response


def exception_format(exc):
    error_list = []
    server_error = ErrorCollection('non_field', '알 수 없는 에러입니다.', 'server_error')

    try:
        if isinstance(exc, APIException):
            _drf_exception_format(exc, error_list)
        else:
            _not_drf_exception_format(exc, error_list)
    except Exception:
        error_list = [vars(server_error)]

    return error_list


def _drf_exception_format(exc, error_list):
    codes = exc.get_codes()

    if isinstance(exc.detail, dict):  # 검증 에러가 필드에서 발생할 때
        for key, value in exc.detail.items():
            if isinstance(value, dict):  # ForeignKey 에서 에러가 나면 한번 더 감싸서 에러가 발생한다.
                for child_key, child_value in value.items():
                    error = ErrorCollection(key, child_value[0], codes[key][child_key][0])
                    error_list.append(vars(error))
            else:
                error = ErrorCollection(key, value[0], codes[key][0])
                error_list.append(vars(error))
    elif isinstance(exc.detail, list):  # 검증 에러가 필드 외에서 발생할 때
        for i in range(0, len(exc.detail)):
            error = ErrorCollection('non_field', exc.detail[i], codes[i])
            error_list.append(vars(error))
    else:  # 검증 에러가 필드 외 단일 에러일 때
        error = ErrorCollection('non_field', exc.detail, codes)
        error_list.append(vars(error))


def _not_drf_exception_format(exc, error_list):
    error = ErrorCollection('non_field', '알 수 없는 에러입니다.', 'server_error')

    if isinstance(exc, OperationalError) and exc.args[0] == 1040:  # max connection 에러
        error = ErrorCollection('non_field', '요청이 너무 많습니다.', 'server_error')
    elif isinstance(exc, Http404):  # 404 에러 리소스가 없을 때 참고 https://stackoverflow.com/questions/3821663/querystring-in-rest-resource-url/3822676#3822676
        error = ErrorCollection('non_field', '리소스를 찾을 수 없습니다.', 'not_found')

    error_list.append(vars(error))
