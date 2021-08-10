from django.utils.encoding import smart_text
from rest_framework import exceptions
from rest_framework.authentication import (
    BaseAuthentication, get_authorization_header
)

from user.auth.serializers import JwtTokenSerializer
from user.models import User


class BaseJSONWebTokenAuthentication(BaseAuthentication):
    """
    Token based authentication using the JSON Web Token standard.
    """

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = self.get_jwt_value(request)

        if jwt_value is None:
            return None

        serializer = JwtTokenSerializer(None, data={'token': jwt_value}, context={'request': request})
        payload = serializer.decode(jwt_value)

        user = self.authenticate_credentials(payload)

        return (user, jwt_value)

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and email.
        """

        if not payload['email']:
            raise exceptions.AuthenticationFailed('잘못된 데이터입니다.')

        try:
            user = User.objects.get_by_natural_key(payload['email'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('잘못된 서명입니다.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('비활성화 상태 혹은 인증되지 않은 계정입니다.')

        return user


class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):
    """
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string specified in the setting
    `Bearer_AUTH_HEADER_PREFIX`. For example:

        Authorization: Bearer eyJhbGciOiAiSFMyNTYiLCAidHlwIj
    """
    www_authenticate_realm = 'api'

    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = 'Bearer'

        if not auth:
            return None

        if smart_text(auth[0]) != auth_header_prefix:
            return None

        if len(auth) == 1:
            raise exceptions.AuthenticationFailed('잘못된 인증 헤더입니다. 제공된 자격 증명이 없습니다.')
        elif len(auth) > 2:
            raise exceptions.AuthenticationFailed('잘못된 인증 헤더입니다. 자격 증명 문자열에는 공백이 없어야합니다.')

        return auth[1]

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return '{0} realm="{1}"'.format('Bearer', self.www_authenticate_realm)
