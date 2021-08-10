
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers
from rest_framework import exceptions
from rest_framework.fields import empty
from common.utils import get_unix_time

from user.auth.enums import TokenType

import jwt
import datetime


class JwtTokenSerializer(serializers.Serializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance=instance, data=data, **kwargs)

    def create_access_token(self, email, token_header={}):
        exp = get_unix_time(timezone.localtime() + datetime.timedelta(minutes=30))

        token_header['email'] = email
        token_header['exp'] = exp
        token_header['type'] = TokenType.ACCESS_TOKEN.value

        return self.encode(token_header)

    def create_refresh_token(self, email, token_header={}):
        exp = get_unix_time(timezone.localtime() + datetime.timedelta(hours=12))

        token_header['email'] = email
        token_header['exp'] = exp
        token_header['type'] = TokenType.REFRESH_TOKEN.value

        return self.encode(token_header)

    def encode(self, payload):
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode()

    def decode(self, token):
        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithm=['HS256'])

            return data
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed('만료된 토큰입니다.')
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed('잘못된 토큰입니다.')


class ObtainJwtTokenSerializer(JwtTokenSerializer):
    email = serializers.EmailField(label='이메일')
    password = serializers.CharField(label='패스워드')

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            token_header = {}
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    raise exceptions.AuthenticationFailed('비활성화 상태 혹은 인증되지 않은 계정입니다.')

                access_token = self.create_access_token(user.email, token_header)
                refresh_token = self.create_refresh_token(user.email)

                return {'access_token': access_token, 'refresh_token': refresh_token}
            else:
                raise exceptions.AuthenticationFailed('로그인에 실패하셨습니다.')


class VerifyJwtTokenSerializer(JwtTokenSerializer):
    access_token = serializers.CharField(allow_blank=True, required=False, label='엑세스 토큰')
    refresh_token = serializers.CharField(allow_blank=True, required=False, label='리프레쉬 토큰')

    def validate_token(self, value):
        data = self.decode(value)

        if data['type'] != TokenType.ACCESS_TOKEN.value:
            raise serializers.ValidationError('토큰 타입이 access_token이 아닙니다.')

        return value

    def validate_refresh_token(self, value):
        data = self.decode(value)

        if data['type'] != TokenType.REFRESH_TOKEN.value:
            raise serializers.ValidationError('토큰 타입이 refresh_token이 아닙니다.')

        return value

    def validate(self, attrs):
        if len(attrs) == 0:
            raise serializers.ValidationError('access_token 혹은 refresh_token을 지정해주세요.')

        return super().validate(attrs)


class RefreshJwtTokenSerializer(JwtTokenSerializer):
    refresh_token = serializers.CharField(label='리프레쉬 토큰')

    def validate_refresh_token(self, value):
        return self.decode(value)

    def validate(self, attrs):
        refresh_token_info = attrs['refresh_token']

        return {'access_token': self.create_access_token(refresh_token_info['email'])}
