from apps.memberships.models import Membership
import threading

class OrganizationMiddleware:
    """
    Middleware que injeta organização e escritório no request.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Inicializa como None
        request.organization = None
        request.office = None
        request.membership = None
        
        # Se usuário está autenticado
        if request.user.is_authenticated:
            membership = Membership.objects.filter(
                user=request.user,
                is_active=True
            ).select_related('organization', 'office').first()
            
            if membership:
                request.organization = membership.organization
                request.office = membership.office
                request.membership = membership
        
        # ⭐ Adicionar request no thread local (para signals)
        threading.current_thread().request = request
        
        response = self.get_response(request)
        
        # Limpar request do thread
        if hasattr(threading.current_thread(), 'request'):
            delattr(threading.current_thread(), 'request')
        
        return response