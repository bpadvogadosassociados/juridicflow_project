# apps/shared/models.py

from django.db import models

class TimestampedModel(models.Model):
    """Adiciona timestamps automáticos"""
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        abstract = True


class OrganizationScopedModel(TimestampedModel):
    """
    Base para models que pertencem a organização + escritório.
    
    IMPORTANTE: Não adicionar indexes aqui (causa problemas em abstract models).
    Adicione indexes nos models concretos se necessário.
    """
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        verbose_name='Organização',
        related_name='%(app_label)s_%(class)s_set'  # ← Evita conflitos
    )
    
    office = models.ForeignKey(
        'offices.Office',
        on_delete=models.CASCADE,
        verbose_name='Escritório',
        related_name='%(app_label)s_%(class)s_set'  # ← Evita conflitos
    )
    
    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """Soft delete"""
    is_deleted = models.BooleanField('Deletado', default=False)
    deleted_at = models.DateTimeField('Deletado em', null=True, blank=True)
    
    class Meta:
        abstract = True

class AuditLog(models.Model):
    """
    Log de auditoria de todas as ações no sistema
    registra quem fez o que e quando.
    """

    ACTION_CHOICES = [
        ('create', 'Criar'),
        ('update', 'Atualizar'),
        ('delete', 'Deletar'),
        ('view', 'Visualizar'),
        ('download', 'Download'),
        ('login', 'Login'),
        ('logout', 'Logout'),
    ]


    # Quem
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        verbose_name='Usuário'
    )
    
    # Onde
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        related_name='audit_logs',
        verbose_name='Organização'
    )
    
    office = models.ForeignKey(
        'offices.Office',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='audit_logs',
        verbose_name='Escritório'
    )
    
    # O quê
    action = models.CharField(
        'Ação',
        max_length=20,
        choices=ACTION_CHOICES
    )
    
    model_name = models.CharField(
        'Model',
        max_length=100,
        help_text='Nome do model afetado'
    )
    
    object_id = models.PositiveIntegerField(
        'ID do Objeto',
        null=True,
        blank=True
    )
    
    object_repr = models.CharField(
        'Representação do Objeto',
        max_length=255,
        blank=True,
        help_text='String representation do objeto'
    )
    
    # Detalhes
    changes = models.JSONField(
        'Alterações',
        default=dict,
        blank=True,
        help_text='Detalhes das alterações (antes/depois)'
    )
    
    ip_address = models.GenericIPAddressField(
        'IP',
        null=True,
        blank=True
    )
    
    user_agent = models.TextField(
        'User Agent',
        blank=True
    )
    
    # Quando
    timestamp = models.DateTimeField(
        'Data/Hora',
        auto_now_add=True,
        db_index=True
    )
    
    class Meta:
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['organization', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['model_name', 'object_id']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.model_name} - {self.timestamp}"