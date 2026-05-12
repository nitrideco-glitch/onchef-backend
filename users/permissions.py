from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        # Check if the object has a 'user' attribute (for food_log and goals)
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # Check if the object is the user itself
        elif hasattr(obj, 'email'):
            return obj == request.user
        
        return False