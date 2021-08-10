from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .serializers import ImageSerializer
from .schemas import image_response_schema


class ImageViewSet(mixins.CreateModelMixin, viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = ImageSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        return self.serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    @extend_schema(request=ImageSerializer, responses={201: image_response_schema})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        headers = self.get_success_headers(serializer.data)

        return Response(result, status=status.HTTP_201_CREATED, headers=headers)
