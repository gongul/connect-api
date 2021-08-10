from rest_framework import routers


class AuthTokenRouter(routers.SimpleRouter):
    routes = [
        routers.Route(
            url=r'^{prefix}/obtain{trailing_slash}$',
            mapping={
                'post': 'obtain',
            },
            name='{basename}-obtain',
            detail=False,
            initkwargs={'suffix': 'Obtain'}
        ),
        routers.Route(
            url=r'^{prefix}/verify{trailing_slash}$',
            mapping={
                'post': 'verify',
            },
            name='{basename}-verify',
            detail=False,
            initkwargs={'suffix': 'Verify'}
        ),
        routers.Route(
            url=r'^{prefix}/refresh{trailing_slash}$',
            mapping={
                'post': 'refresh',
            },
            name='{basename}-refresh',
            detail=False,
            initkwargs={'suffix': 'Refresh'}
        ),
    ]
