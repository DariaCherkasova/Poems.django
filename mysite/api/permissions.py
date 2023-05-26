from rest_framework import permissions

class UserOrReadOnly(permissions.BasePermission):
    '''проверка безопасности метода (чтобы был get/head/options) и аутентификации'''
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)
    '''если has_permission=true, то выполняем'''
    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user)

class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
