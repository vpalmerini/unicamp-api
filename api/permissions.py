from rest_framework import permissions


class IsSafeOrIsStaff(permissions.BasePermission):
    """
    Allow only GET requests for non admins
    """
    def has_permission(self, request, view):
        # allow all GET requests
        if request.method == 'GET':
            return True
        # otherwise, will allow only admin requests
        return request.user and request.user.is_staff
