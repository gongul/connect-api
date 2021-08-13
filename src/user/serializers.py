from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework import exceptions
from rest_framework_miem.serializers import InheritsModelSerializer

from common.utils import EmailThread
from common.views import ActionEnum
from user.validator.message import UserValidationMessage

from .models import Friend, User

from random import random


class ActivateSerializer(InheritsModelSerializer):
    def update(self, instance, validated_data):
        validated_data['is_verified'] = True
        validated_data['is_active'] = True

        if instance.verifying_number != validated_data['verifying_number']:
            raise serializers.ValidationError(UserValidationMessage.VERIFYING_NUMBER.invalid)

        validated_data['verifying_number'] = None

        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ['verifying_number']
        extra_kwargs = {
            'verifying_number': {'write_only': True, 'required': True, 'min_length': 6},
        }


class UserSerializer(InheritsModelSerializer):
    def validate(self, attrs):
        request = self.context['request']
        errors = {}
        validate_fields = ['is_verified', 'is_active']

        for field in validate_fields:
            validate_data = attrs.get(field, None)
            if validate_data is not None and not request.user.is_staff:
                errors[field] = [exceptions.PermissionDenied.default_detail]

        if errors:
            raise exceptions.PermissionDenied(errors)

        return attrs

    def validate_password(self, value):
        password = make_password(value)

        return password

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'registration_date', 'is_verified', 'is_active']
        read_only_fields = ['registration_date', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class FriendSerializer(InheritsModelSerializer):
    # not required : request_date accept_date
    # def get_fields(self):
    #     fields = super().get_fields()

    #     if self.context == {}:
    #         return fields

    #     action = self.context['view'].action
    #     request = self.context['request']

    #     # fields['request_date'].read_only = True
    #     # fields['accept_date'].read_only = True

    #     # if not request.user.is_staff and action == ActionEnum.CREATE.value:
    #     #     fields['is_friend'].read_only = True
    #     # elif not request.user.is_staff and action in [ActionEnum.UPDATE.value, ActionEnum.PARTIAL_UPDATE.value]:
    #     #     fields['friend_user'].read_only = True

    #     return fields

    def validate_is_friend(self, value):
        request_user = self.context['request'].user

        if not request_user.is_staff and value != request_user:
            raise exceptions.PermissionDenied({'is_friend': [exceptions.PermissionDenied.default_detail]})
        elif value == request_user and value == 0:
            raise exceptions.PermissionDenied({'is_friend': [exceptions.PermissionDenied.default_detail]})

        return value

    def validate_request_date(self, value):
        if not self.context['request'].user.is_staff:
            raise exceptions.PermissionDenied({'request_date': [exceptions.PermissionDenied.default_detail]})

        return value

    def validate_accept_date(self, value):
        if not self.context['request'].user.is_staff:
            raise exceptions.PermissionDenied({'accept_date': [exceptions.PermissionDenied.default_detail]})

        return value

    def validate_friend_user(self, value):
        action = self.context['view'].action

        if not self.context['request'].user.is_staff and action in [ActionEnum.UPDATE.value, ActionEnum.PARTIAL_UPDATE.value]:
            raise exceptions.PermissionDenied({'friend_user': [exceptions.PermissionDenied.default_detail]})

        return value

    def validate(self, attrs):
        action = self.context['view'].action
        request_user = self.context['request'].user

        if action == ActionEnum.CREATE.value:
            attrs['user'] = request_user

        return attrs

    class Meta:
        model = Friend
        fields = '__all__'
        read_only_fields = ['user']
        extra_kwargs = {
            'request_date': {'required': False},
            'accept_date': {'required': False},
            'is_friend': {'required': False},
            'friend_user': {'required': False},
        }


class SignupSerializer(InheritsModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        normalize_email = UserManager.normalize_email(value)

        return normalize_email

    def validate_password(self, value):
        password = make_password(value)

        return password

    def create(self, validated_data):
        validated_data['verifying_number'] = str(random()).replace(".", "")[:6]

        return super().create(validated_data)

    def send_activate_email(self):
        user = self.instance

        subject = ('[connect] 인증 번호')
        message = render_to_string('user/verifying_number.html', {
            'verifying_number': user.verifying_number
        })
        EmailThread(subject, message, [user.email], html=message).start()
