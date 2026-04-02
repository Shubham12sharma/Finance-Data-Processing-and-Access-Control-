from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    """Only users with 'admin' role can access"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and request.user.role == 'admin'
        )


class IsAnalystOrHigher(BasePermission):
    """Analyst and Admin can access"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and request.user.role in ['analyst', 'admin']
        )


class IsOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has a `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.user == request.user


class IsViewerOrHigher(BasePermission):
    """All authenticated users (Viewer, Analyst, Admin)"""
    def has_permission(self, request, view):
        return request.user.is_authenticated