from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff

class IsActiveUserOnly(BasePermission):
    def has_permission(self, request, view) -> bool:
        print(SAFE_METHODS)
        return request.user.is_active

class IsNamedUserOnly(BasePermission):
    def is_name_good(self, name):
        result: bool = name != ""
        print(f'name: {name}, is_name: {result}')
        return result

    def has_permission(self, request, view) -> bool:

        return self.is_name_good(request.user.first_name)
