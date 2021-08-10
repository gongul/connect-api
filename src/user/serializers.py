from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from rest_framework import serializers
from rest_framework import exceptions
from rest_framework_miem.serializers import InheritsModelSerializer

from common.utils import EmailThread
from user.validator.message import UserValidationMessage

from .models import User

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
