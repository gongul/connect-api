from django.urls import include, path

from rest_framework_nested import routers

from . import views

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'images', views.ImageViewSet, basename='images')

image_patterns = ([
    path('', include(router.urls))
])
