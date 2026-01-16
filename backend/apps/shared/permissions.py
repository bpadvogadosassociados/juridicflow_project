# apps/shared/permissions.py

from django.core.exceptions import PermissionDenied

class BasePermission:
    """
    Base para permissões customizadas.
    """
    
    def has_permission(self, user, organization=None, office=None):
        """Verifica se usuário tem permissão genérica"""
        return False
    
    def has_object_permission(self, user, obj):
        """Verifica se usuário tem permissão sobre objeto específico"""
        return False


class IsOrganizationAdmin(BasePermission):
    """Apenas Organization Admin"""
    
    def has_permission(self, user, organization=None, office=None):
        from apps.memberships.models import Membership
        
        return Membership.objects.filter(
            user=user,
            organization=organization,
            role='org_admin',
            is_active=True
        ).exists()


class IsOfficeAdmin(BasePermission):
    """Organization Admin ou Office Admin"""
    
    def has_permission(self, user, organization=None, office=None):
        from apps.memberships.models import Membership
        
        return Membership.objects.filter(
            user=user,
            organization=organization,
            role__in=['org_admin', 'office_admin'],
            is_active=True
        ).exists()


class CanManageCustomers(BasePermission):
    """Pode gerenciar clientes"""
    
    def has_permission(self, user, organization=None, office=None):
        from apps.memberships.models import Membership
        
        return Membership.objects.filter(
            user=user,
            organization=organization,
            role__in=['org_admin', 'office_admin', 'lawyer'],
            is_active=True
        ).exists()


class CanManageProcesses(BasePermission):
    """Pode gerenciar processos"""
    
    def has_permission(self, user, organization=None, office=None):
        from apps.memberships.models import Membership
        
        return Membership.objects.filter(
            user=user,
            organization=organization,
            role__in=['org_admin', 'office_admin', 'lawyer'],
            is_active=True
        ).exists()


class CanViewConfidential(BasePermission):
    """Pode ver documentos/processos confidenciais"""
    
    def has_permission(self, user, organization=None, office=None):
        from apps.memberships.models import Membership
        
        return Membership.objects.filter(
            user=user,
            organization=organization,
            role__in=['org_admin', 'office_admin', 'lawyer'],
            is_active=True
        ).exists()
    
    def has_object_permission(self, user, obj):
        """Verifica se pode ver este objeto específico"""
        # Se não é confidencial, qualquer um pode ver
        if hasattr(obj, 'is_confidential') and not obj.is_confidential:
            return True
        
        # Se é confidencial, precisa ser admin ou lawyer
        from apps.memberships.models import Membership
        return Membership.objects.filter(
            user=user,
            organization=obj.organization,
            role__in=['org_admin', 'office_admin', 'lawyer'],
            is_active=True
        ).exists()


# Helper function
def check_permission(user, permission_class, organization=None, office=None, obj=None):
    """
    Verifica permissão de forma simples.
    
    Uso:
        if check_permission(request.user, CanManageCustomers, request.organization):
            # faz algo
    """
    permission = permission_class()
    
    if obj:
        return permission.has_object_permission(user, obj)
    else:
        return permission.has_permission(user, organization, office)