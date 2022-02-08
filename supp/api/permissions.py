from rest_framework import permissions
from .service import is_spamer

class OnlyOwnObjects(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj)
        print('test')
        return bool(request.user.is_staff or obj.user == request.user)

class IsNotSpamer(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action == 'create':
            print('test')
            return bool(is_spamer(obj) and request.user.is_staff is False)




