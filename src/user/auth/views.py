from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response

from user.auth.serializers import ObtainJwtTokenSerializer, RefreshJwtTokenSerializer, VerifyJwtTokenSerializer
from user.auth.schemas import refresh_response_schema, obtain_response_schema


class Obtain():
    @extend_schema(request=ObtainJwtTokenSerializer,
                   responses={201: obtain_response_schema})
    def obtain(self, request, *args, **kwargs):
        serializer = ObtainJwtTokenSerializer(None, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)


class Verify():
    @extend_schema(request=VerifyJwtTokenSerializer,
                   responses={201: VerifyJwtTokenSerializer})
    def verify(self, request, *args, **kwargs):
        serializer = VerifyJwtTokenSerializer(None, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)


class Refresh():
    @extend_schema(request=RefreshJwtTokenSerializer,
                   responses={201: refresh_response_schema})
    def refresh(self, request, *args, **kwargs):
        serializer = RefreshJwtTokenSerializer(None, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)


class JwtTokenViewSet(viewsets.ViewSet, Obtain, Verify, Refresh):
    pass
