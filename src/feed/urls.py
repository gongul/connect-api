from django.urls import include, path

from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'feeds', views.FeedViewSet)

feed_patterns = ([
    path('', include(router.urls))
])
