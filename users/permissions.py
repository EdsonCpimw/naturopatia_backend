from rest_framework import permissions
from rest_framework.permissions import DjangoModelPermissions
from rest_framework import exceptions


class EditPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        pk = int(view.kwargs.get('pk'))
        if request.user.tipo_usuario == request.user.USUARIO:
            if view.action == 'retrieve' or view.action == 'update':
                if request.user.id == pk:
                    return True
        elif request.user.tipo_usuario == request.user.ADMINISTRADOR:
            return True



class UsuarioPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.tipo_usuario == request.user.ADMINISTRADOR:
            return True
        elif request.user.tipo_usuario == request.user.USUARIO:
            return True

        else:
            return False


class AdministradorPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif request.user.tipo_usuario == request.user.ADMINISTRADOR:
                return True

