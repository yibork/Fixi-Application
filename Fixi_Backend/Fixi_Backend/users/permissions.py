from rest_framework import permissions
from .models import User

class IsServiceProvider(permissions.BasePermission):
    """
    Custom permission to only allow service providers to access a view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.role == User.ServiceProvider
