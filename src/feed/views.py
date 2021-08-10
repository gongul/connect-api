from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser

from feed.models import Feed
from feed.serializers import FeedSerializer

# Create your views here.


class FeedViewSet(viewsets.ModelViewSet):
    queryset = Feed.objects.all()
    permission_classes = []
    serializer_class = FeedSerializer
    parser_classes = [MultiPartParser]
