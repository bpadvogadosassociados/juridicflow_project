from django.db import models

class OrganizationScopedManager(models.Manager):
    """
    Manager que filtra automaticamente por organização e escritório.
    
    Uso:
        Customer.objects.for_request(request)
        # Retorna só customers da org/office do request
    """
    
    def for_request(self, request):
        """
        Filtra por organização e escritório do request.
        """
        if not hasattr(request, 'organization') or not request.organization:
            # Se não tem organização no request, retorna vazio (segurança)
            return self.none()
        
        queryset = self.filter(organization=request.organization)
        
        # Se tem office no request, filtra também por office
        if hasattr(request, 'office') and request.office:
            queryset = queryset.filter(office=request.office)
        
        return queryset
    
    def for_organization(self, organization):
        """
        Filtra por organização específica.
        Útil para tarefas administrativas.
        """
        return self.filter(organization=organization)
    
    def for_office(self, office):
        """
        Filtra por escritório específico.
        """
        return self.filter(office=office)


class SoftDeleteManager(models.Manager):
    """
    Manager que exclui automaticamente itens deletados (soft delete).
    """
    
    def get_queryset(self):
        """Por padrão, não retorna itens deletados"""
        return super().get_queryset().filter(is_deleted=False)
    
    def with_deleted(self):
        """Retorna tudo, incluindo deletados"""
        return super().get_queryset()
    
    def deleted_only(self):
        """Retorna só os deletados"""
        return super().get_queryset().filter(is_deleted=True)