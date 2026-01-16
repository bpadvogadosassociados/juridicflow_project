from django.db import models
from apps.shared.models import OrganizationScopedModel
from apps.shared.managers import OrganizationScopedManager
import re
from django.core.exceptions import ValidationError

def validate_document(value):
    """Valida formato básico de CPF/CNPJ"""
    # Remove caracteres não numéricos
    clean = re.sub(r'[^0-9]', '', value)
    
    if len(clean) not in [11, 14]:
        raise ValidationError('CPF deve ter 11 dígitos ou CNPJ 14 dígitos')
    
    return clean

class Customer(OrganizationScopedModel):
    """
    Cliente do escritório (pessoa física ou jurídica).
    Pode ser autor, réu ou terceiro em processos.
    """
    
    TYPE_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    ]
    
    # ===== INFORMAÇÕES BÁSICAS =====
    name = models.CharField(
        'Nome/Razão Social',
        max_length=255,
        help_text='Nome completo (PF) ou Razão Social (PJ)'
    )
    
    type = models.CharField(
        'Tipo',
        max_length=2,
        choices=TYPE_CHOICES,
        default='PF'
    )
    
    document = models.CharField(
        'CPF/CNPJ',
        max_length=20,
        validators=[validate_document],
        help_text='CPF (XXX.XXX.XXX-XX) ou CNPJ (XX.XXX.XXX/XXXX-XX)'
    )
    
    def save(self, *args, **kwargs):
        # Limpa o documento antes de salvar
        if self.document:
            self.document = re.sub(r'[^0-9]', '', self.document)
        super().save(*args, **kwargs)

    # ===== CONTATO =====
    email = models.EmailField(
        'Email',
        blank=True,
        help_text='Email principal'
    )
    
    phone = models.CharField(
        'Telefone',
        max_length=20,
        blank=True,
        help_text='Telefone principal'
    )
    
    phone_secondary = models.CharField(
        'Telefone Secundário',
        max_length=20,
        blank=True
    )
    
    # ===== ENDEREÇO =====
    address = models.CharField(
        'Endereço',
        max_length=500,
        blank=True
    )
    
    city = models.CharField(
        'Cidade',
        max_length=100,
        blank=True
    )
    
    state = models.CharField(
        'Estado',
        max_length=2,
        blank=True,
        help_text='UF (ex: SP, RJ)'
    )
    
    zip_code = models.CharField(
        'CEP',
        max_length=10,
        blank=True
    )
    
    # ===== OBSERVAÇÕES =====
    notes = models.TextField(
        'Observações',
        blank=True,
        help_text='Anotações internas sobre o cliente'
    )
    
    # ===== STATUS =====
    is_active = models.BooleanField(
        'Ativo',
        default=True,
        help_text='Cliente ativo no sistema'
    )
    
    # Manager customizado (herda filtros automáticos)
    objects = OrganizationScopedManager()
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-created_at']
        # Garante que não tem cliente duplicado na mesma org
        unique_together = [['organization', 'document']]
        indexes = [
            models.Index(fields=['organization', 'office']),
            models.Index(fields=['document']),
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.document})"
    
    @property
    def document_formatted(self):
        """Retorna documento formatado"""
        if self.type == 'PF' and len(self.document) == 11:
            # CPF: XXX.XXX.XXX-XX
            return f"{self.document[:3]}.{self.document[3:6]}.{self.document[6:9]}-{self.document[9:]}"
        elif self.type == 'PJ' and len(self.document) == 14:
            # CNPJ: XX.XXX.XXX/XXXX-XX
            return f"{self.document[:2]}.{self.document[2:5]}.{self.document[5:8]}/{self.document[8:12]}-{self.document[12:]}"
        return self.document

    @property
    def total_processes(self):
        """Retorna total de processos associados ao cliente"""
        return self.process_parties.values('process').distinct().count()