from rest_framework import permissions

class IsDirectivoOrSuperadmin(permissions.BasePermission):
    """
    Permite el acceso solo a usuarios con rol DIRECTIVO o SUPERADMIN.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.rol in ['DIRECTIVO', 'SUPERADMIN'])

class IsMaestro(permissions.BasePermission):
    """
    Permite el acceso a usuarios con rol MAESTRO.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.rol == 'MAESTRO')