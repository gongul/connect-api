from drf_spectacular.extensions import OpenApiAuthenticationExtension


class BearerAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'user.auth.authentications.JSONWebTokenAuthentication'  # full import path OR class ref
    name = 'Bearer'  # name used in the schema

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer'
        }
