from rest_framework import permissions


class OnlyOwnObjects(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj)
        print('test onlyown')
        return bool(request.user.is_staff or obj.user == request.user)

