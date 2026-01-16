# apps/offices/models.py

from django.db import models
from apps.organizations.models import Organization

class Office(models.Model):
    """
    Escritório ou filial de uma organização.
    Exemplo: Matriz SP, Filial RJ, Departamento Trabalhista
    """
    
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='offices',
        verbose_name='Organização'
    )
    
    name = models.CharField(
        'Nome',
        max_length=255,
        help_text='Nome do escritório/filial'
    )
    
    # Opcional: endereço, contato, etc (adicionar depois se quiser)
    # address = models.CharField('Endereço', max_length=500, blank=True)
    # phone = models.CharField('Telefone', max_length=20, blank=True)
    
    # Configurações flexíveis (igual Organization)
    settings = models.JSONField(
        'Configurações',
        default=dict,
        blank=True,
        help_text='Configurações específicas do escritório'
    )
    
    is_active = models.BooleanField(
        'Ativo',
        default=True,
        help_text='Escritório ativo'
    )
    
    # Datas
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Escritório'
        verbose_name_plural = 'Escritórios'
        ordering = ['-created_at']
        # Garante que não tem escritório duplicado na mesma org
        unique_together = [['organization', 'name']]
    
    def __str__(self):
        return f"{self.name} ({self.organization.name})"