from rest_framework import permissions
from apps.shared.permissions import (
    IsOrganizationAdmin,
    IsOfficeAdmin,
    CanManageCustomers,
    CanManageProcesses,
    CanViewConfidential
)

class IsOrganizationAdminPermission(permissions.BasePermission):
    """
    Permissão DRF para Organization Admin.
    """
    message = "Você precisa ser Organization Admin."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        permission = IsOrganizationAdmin()
        return permission.has_permission(
            request.user,
            request.organization,
            request.office
        )


class IsOfficeAdminPermission(permissions.BasePermission):
    """
    Permissão DRF para Office Admin ou Organization Admin.
    """
    message = "Você precisa ser Office Admin ou Organization Admin."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        permission = IsOfficeAdmin()
        return permission.has_permission(
            request.user,
            request.organization,
            request.office
        )


class CanManageCustomersPermission(permissions.BasePermission):
    """
    Permissão DRF para gerenciar clientes.
    """
    message = "Você não tem permissão para gerenciar clientes."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Leitura: qualquer autenticado
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Escrita: org_admin, office_admin, lawyer
        permission = CanManageCustomers()
        return permission.has_permission(
            request.user,
            request.organization,
            request.office
        )


class CanManageProcessesPermission(permissions.BasePermission):
    """
    Permissão DRF para gerenciar processos.
    """
    message = "Você não tem permissão para gerenciar processos."
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        permission = CanManageProcesses()
        return permission.has_permission(
            request.user,
            request.organization,
            request.office
        )


class CanViewConfidentialPermission(permissions.BasePermission):
    """
    Permissão DRF para ver documentos/processos confidenciais.
    """
    message = "Você não tem permissão para acessar conteúdo confidencial."
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        permission = CanViewConfidential()
        return permission.has_object_permission(request.user, obj)