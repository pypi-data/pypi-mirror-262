from .viewsets import UserViewSet, GroupViewSet, PermissionViewSet

#
try:
    from django.conf import settings.DRF_ROUTER as drf_router

    drf_router.register('users/user', UserViewSet, basename='users-user')
    drf_router.register('users/group', GroupViewSet, basename='users-group')
    drf_router.register('users/permission', PermissionViewSet, basename='users-permission')

except ImportError:
    pass



