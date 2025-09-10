
from rest_framework.permissions import BasePermission

class RolePermissions(BasePermission):
    def has_permission(self, request, view):
        if request.user.role.Name.lower() == "admin" and request.method in ["GET","POST","PUT",'DELETE']:
            return True
        if request.user.role.Name.lower() == "employee" and request.method in ["GET","POST"]:
            return True
        if request.user.role.Name.lower() == "stack_holder" and request.method in ["GET"]:
            return True

        return False