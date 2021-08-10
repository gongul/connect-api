from django.urls import include, path

from rest_framework_nested import routers

from user.auth.routers import AuthTokenRouter
from user.auth.views import JwtTokenViewSet

from . import views


auth_router = AuthTokenRouter(trailing_slash=False)

auth_router.register(r'auth', JwtTokenViewSet, basename='auth')

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'users', views.UserViewSet)

user_patterns = ([
    path('', include(auth_router.urls)),
    path('signup', views.SignupView.as_view(), name='signup'),
    path('', include(router.urls))
])
