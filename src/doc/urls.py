from django.urls import path

from . import views

doc_patterns = [
    path('docs/login', views.DocLoginView.as_view(), name='doc-login'),
    path('docs/schema', views.CustomSpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger', views.CustomSpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/redoc', views.CustomSpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
