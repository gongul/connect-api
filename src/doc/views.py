from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls.base import reverse
from rest_framework.authentication import SessionAuthentication
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


class DocLoginView(LoginView):
    template_name = 'admin/login.html'
    authentication_form = AuthenticationForm

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse('redoc')


class CustomSpectacularAPIView(SpectacularAPIView):
    authentication_classes = [SessionAuthentication]


class CustomSpectacularRedocView(SpectacularRedocView):
    authentication_classes = [SessionAuthentication]


class CustomSpectacularSwaggerView(SpectacularSwaggerView):
    authentication_classes = [SessionAuthentication]
