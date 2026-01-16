# apps/memberships/models.py

from django.db import models
from apps.accounts.models import User
from apps.organizations.models import Organization
from apps.offices.models import Office

class Membership(models.Model):
    """
    Vínculo entre User, Organization, Office e Role.
    """
    
    ROLE_CHOICES = [
        ('org_admin', 'Organization Admin'),
        ('office_admin', 'Office Admin'),
        ('lawyer', 'Advogado'),
        ('intern', 'Estagiário'),
        ('accountant', 'Contador'),
        ('finance', 'Financeiro'),
        ('guest', 'Convidado'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name='Usuário'
    )
    
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name='Organização'
    )
    
    office = models.ForeignKey(
        Office,
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name='Escritório',
        null=True,
        blank=True
    )
    
    role = models.CharField(
        'Papel',
        max_length=20,
        choices=ROLE_CHOICES,
        default='guest',  # ← Adicionar default
        help_text='Função do usuário nesta organização/escritório'
    )
    
    is_active = models.BooleanField(
        'Ativo',
        default=True,
        help_text='Membership ativo'
    )
    
    settings = models.JSONField(
        'Configurações',
        default=dict,
        blank=True,
        help_text='Configurações específicas deste membership'
    )
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Membership'
        verbose_name_plural = 'Memberships'
        ordering = ['-created_at']
        unique_together = [['user', 'organization', 'office']]
    
    def __str__(self):
        office_name = self.office.name if self.office else "Todas"
        return f"{self.user.email} - {self.role} em {office_name}"