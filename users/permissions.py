from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """Only Admin can access"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAnalystOrHigher(BasePermission):
    """Analyst and Admin"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_analyst


class IsOwnerOrReadOnly(BasePermission):
    """Users can only modify their own data"""
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj.user == request.user if hasattr(obj, 'user') else obj == request.user