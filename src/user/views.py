from django.db import transaction
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from common.filters import CustomOrderingFilterBackends

from common.permissions import IsAdminUser
from user.filters import FriendFilter, UserFilter
from user.permissions import IsFriendOwner, IsUserOwner

from .models import Friend, User
from .serializers import ActivateSerializer, FriendSerializer, SignupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    default_limit = 50
    lookup_value_regex = '[^/]+'
    filter_backends = [DjangoFilterBackend, CustomOrderingFilterBackends]
    ordering_fields = ['registration_date', 'is_active', 'is_verified']
    permission_classes = [IsUserOwner | IsAdminUser]
    filter_class = UserFilter

    @extend_schema(operation_id='users_activate', description='인증번호로 해당 유저를 활성화 시킨다.', responses={'204': None})
    @action(url_name='activate', url_path='activate', detail=True,
            serializer_class=ActivateSerializer, authentication_classes=[],
            permission_classes=[], methods=['POST'])
    def activate(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendViewSet(viewsets.ModelViewSet):
    queryset = Friend.objects.select_related('user', 'friend_user')
    serializer_class = FriendSerializer
    default_limit = 50
    filter_backends = [DjangoFilterBackend, CustomOrderingFilterBackends]
    ordering_fields = ['id', 'request_date']
    permission_classes = [IsFriendOwner | IsAdminUser]
    filter_class = FriendFilter

    @extend_schema(operation_id='friends_my_friends', description='내 친구목록을 보여준다.')
    @action(url_name='my-friends', url_path='my-friends', detail=False, methods=['GET'])
    def my_friends(self, request, *args, **kwargs):
        self.filter_class = None
        self.queryset = self.queryset.filter(Q(user=self.request.user) | Q(friend_user=self.request.user))

        return super().list(request, *args, **kwargs)


class SignupView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = SignupSerializer

    @extend_schema(operation_id='signup')
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        serializer.send_activate_email()
