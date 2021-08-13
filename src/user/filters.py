from django import forms
from rest_framework import exceptions
from django_filters import rest_framework
from django_filters.rest_framework import filters

from .models import Friend, User


class UserFilter(rest_framework.FilterSet):
    email = filters.CharFilter(field_name='email', lookup_expr='contains')
    name = filters.CharFilter(field_name='name', lookup_expr='contains')
    registration_date = filters.DateFromToRangeFilter(field_name='registration_date')

    class Meta:
        model = User
        fields = ['email', 'name', 'is_verified', 'is_active', 'registration_date']


class FriendFilterForm(forms.Form):
    def clean_is_friend(self):
        is_friend = self.cleaned_data['is_friend']
        request_user = self.request.user

        if not request_user.is_staff and is_friend != 0:
            raise exceptions.PermissionDenied()

        return is_friend

    def clean_user__email(self):
        email = self.cleaned_data['user__email']
        request_user = self.request.user

        if email != '' and email != request_user.email:
            raise exceptions.PermissionDenied()

        return email

    def clean_friend_user__email(self):
        email = self.cleaned_data['friend_user__email']
        request_user = self.request.user.email

        if email != '' and email != request_user:
            raise exceptions.PermissionDenied()

        return email


class FriendFilter(rest_framework.FilterSet):
    user__email = filters.CharFilter(field_name='user__email', lookup_expr='contains')
    friend_user__email = filters.CharFilter(field_name='friend_user__email', lookup_expr='contains')
    request_date = filters.DateFromToRangeFilter(field_name='request_date')

    @property
    def form(self):
        form = super().form
        form.request = self.request

        return form

    class Meta:
        model = Friend
        form = FriendFilterForm
        fields = ['user__email', 'friend_user__email', 'is_friend', 'request_date']
