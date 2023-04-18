from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(obj.author == request.user and request.user.is_authenticated
                    or request.user.is_staff)
        
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True 
        
        return bool(request.user.is_authenticated or request.user.is_staff)