from rest_framework import permissions
from django.urls import reverse
from copy import deepcopy


class CustomPermissions(permissions.BasePermission):
    """Permisos si contiene el codename de la funcion en el grupo."""
    def has_permission(self, request, view):
        """Sobre escritura del metodo has_permissions."""
        groups = request.user.groups.first()  # Grupo asociado

        if groups:
            permission_mapping = {
                'create': 'add',
                'list': 'view',
                'retrieve': 'view',
                'update': 'change',
                'partial_update': 'change',
                'destroy': 'delete',
                'get': 'view',
                'post': 'add',
                'put': 'change',
                'delete': 'delete'
            }
            request_method = request.META[
                "REQUEST_METHOD"]  # Tipo de metodo(get,post,put,delete)
            request_action = view.action  # Nombre del metodo

            if view.model != None:
                request_model = view.model._meta.verbose_name  # verbose_name del modelo

            permiso = f"Can {permission_mapping.get(request_method.lower(),request_action)} {request_model if request_action in permission_mapping or view.model is not None else request_action}"
            """Validar si el permiso esta en la lista de permisos del grupo."""
            if permiso in groups.permissions.values_list('name', flat=True):
                return True
            return False
        return False
