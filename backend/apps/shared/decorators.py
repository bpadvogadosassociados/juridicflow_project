from functools import wraps
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

def organization_admin_required(view_func):
    """
    Decorator que exige Organization Admin.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin:login')
        
        from apps.shared.permissions import IsOrganizationAdmin
        
        if not IsOrganizationAdmin().has_permission(
            request.user,
            request.organization
        ):
            raise PermissionDenied("Você não tem permissão para acessar esta página.")
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def office_admin_required(view_func):
    """
    Decorator que exige Office Admin ou Organization Admin.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin:login')
        
        from apps.shared.permissions import IsOfficeAdmin
        
        if not IsOfficeAdmin().has_permission(
            request.user,
            request.organization,
            request.office
        ):
            raise PermissionDenied("Você não tem permissão para acessar esta página.")
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def permission_required(permission_class):
    """
    Decorator genérico para permissões customizadas.
    
    Uso:
        @permission_required(CanManageCustomers)
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('admin:login')
            
            permission = permission_class()
            if not permission.has_permission(
                request.user,
                request.organization,
                request.office
            ):
                raise PermissionDenied("Você não tem permissão.")
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator