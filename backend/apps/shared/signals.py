from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from apps.shared.models import AuditLog
import json

# Lista de models que devem ser auditados
AUDITED_MODELS = [
    'Customer',
    'Process',
    'ProcessParty',
    'Deadline',
    'Document',
    'Organization',
    'Office',
    'Membership',
]


def get_request():
    """
    Pega o request atual do thread local.
    Será configurado no middleware.
    """
    import threading
    return getattr(threading.current_thread(), 'request', None)


def get_changes(instance, old_instance=None):
    """
    Calcula as mudanças entre versões do objeto.
    """
    if not old_instance:
        return {'action': 'created'}
    
    changes = {}
    for field in instance._meta.fields:
        field_name = field.name
        
        # Pula campos de auditoria
        if field_name in ['created_at', 'updated_at', 'id']:
            continue
        
        old_value = getattr(old_instance, field_name, None)
        new_value = getattr(instance, field_name, None)
        
        # Serializa valores complexos
        if hasattr(old_value, 'pk'):
            old_value = str(old_value)
        if hasattr(new_value, 'pk'):
            new_value = str(new_value)
        
        if old_value != new_value:
            changes[field_name] = {
                'old': str(old_value) if old_value is not None else None,
                'new': str(new_value) if new_value is not None else None,
            }
    
    return changes


@receiver(post_save)
def audit_post_save(sender, instance, created, **kwargs):
    """
    Audita criação e atualização de objetos.
    """
    # Verifica se é um model auditado
    if sender.__name__ not in AUDITED_MODELS:
        return
    
    # Verifica se tem AuditLog (evita loop infinito)
    if sender.__name__ == 'AuditLog':
        return
    
    # Pega o request
    request = get_request()
    if not request or not request.user.is_authenticated:
        return
    
    # Pega organização e office
    organization = getattr(request, 'organization', None)
    office = getattr(request, 'office', None)
    
    # Se o objeto tem organization, usa ela
    if hasattr(instance, 'organization'):
        organization = instance.organization
    if hasattr(instance, 'office'):
        office = instance.office
    
    if not organization:
        return
    
    # Determina a ação
    action = 'create' if created else 'update'
    
    # Calcula mudanças (para updates)
    changes = {}
    if not created and hasattr(instance, '_old_instance'):
        changes = get_changes(instance, instance._old_instance)
    
    # IP do usuário
    ip_address = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # Cria log
    try:
        AuditLog.objects.create(
            user=request.user,
            organization=organization,
            office=office,
            action=action,
            model_name=sender.__name__,
            object_id=instance.pk,
            object_repr=str(instance)[:255],
            changes=changes,
            ip_address=ip_address,
            user_agent=user_agent[:500] if user_agent else ''
        )
    except Exception as e:
        # Não falha a operação principal se auditoria falhar
        print(f"Erro ao criar audit log: {e}")


@receiver(post_delete)
def audit_post_delete(sender, instance, **kwargs):
    """
    Audita deleção de objetos.
    """
    # Verifica se é um model auditado
    if sender.__name__ not in AUDITED_MODELS:
        return
    
    if sender.__name__ == 'AuditLog':
        return
    
    request = get_request()
    if not request or not request.user.is_authenticated:
        return
    
    organization = getattr(request, 'organization', None)
    office = getattr(request, 'office', None)
    
    if hasattr(instance, 'organization'):
        organization = instance.organization
    if hasattr(instance, 'office'):
        office = instance.office
    
    if not organization:
        return
    
    ip_address = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    try:
        AuditLog.objects.create(
            user=request.user,
            organization=organization,
            office=office,
            action='delete',
            model_name=sender.__name__,
            object_id=instance.pk,
            object_repr=str(instance)[:255],
            ip_address=ip_address,
            user_agent=user_agent[:500] if user_agent else ''
        )
    except Exception as e:
        print(f"Erro ao criar audit log: {e}")


@receiver(pre_save)
def store_old_instance(sender, instance, **kwargs):
    """
    Armazena versão antiga do objeto antes de salvar (para detectar mudanças).
    """
    if sender.__name__ not in AUDITED_MODELS:
        return
    
    if sender.__name__ == 'AuditLog':
        return
    
    if instance.pk:
        try:
            instance._old_instance = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            instance._old_instance = None
    else:
        instance._old_instance = None