# apps/documents/models.py

from django.db import models
from apps.shared.models import OrganizationScopedModel
from apps.shared.managers import OrganizationScopedManager
from apps.accounts.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import os

def document_upload_path(instance, filename):
    """
    Define o caminho de upload dos documentos.
    Organiza por: organization/office/ano/mes/filename
    """
    from datetime import datetime
    now = datetime.now()
    org_id = instance.organization.id
    office_id = instance.office.id
    year = now.year
    month = now.month
    
    return f'documents/org_{org_id}/office_{office_id}/{year}/{month:02d}/{filename}'

class Document(OrganizationScopedModel):
    """
    Documento do escritório.
    Pode ser vinculado a processo, cliente, etc.
    """
    
    CATEGORY_CHOICES = [
        ('petition', 'Petição'),
        ('contract', 'Contrato'),
        ('decision', 'Decisão Judicial'),
        ('proof', 'Prova'),
        ('correspondence', 'Correspondência'),
        ('invoice', 'Nota Fiscal'),
        ('receipt', 'Recibo'),
        ('procuration', 'Procuração'),
        ('report', 'Relatório'),
        ('other', 'Outro'),
    ]
    
    # ===== INFORMAÇÕES BÁSICAS =====
    title = models.CharField(
        'Título',
        max_length=255,
        help_text='Nome/descrição do documento'
    )
    
    category = models.CharField(
        'Categoria',
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other'
    )
    
    description = models.TextField(
        'Descrição',
        blank=True,
        help_text='Descrição detalhada do documento'
    )
    
    # ===== ARQUIVO =====
    file = models.FileField(
        'Arquivo',
        upload_to=document_upload_path,
        help_text='Arquivo do documento (PDF, DOCX, imagem, etc)'
    )
    
    file_size = models.PositiveIntegerField(
        'Tamanho',
        null=True,
        blank=True,
        help_text='Tamanho do arquivo em bytes'
    )
    
    # ===== VINCULAÇÃO GENÉRICA =====
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Tipo de Objeto'
    )
    
    object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='ID do Objeto'
    )
    
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # ===== CONTROLE =====
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_documents',
        verbose_name='Enviado por'
    )
    
    is_confidential = models.BooleanField(
        'Confidencial',
        default=False,
        help_text='Documento confidencial (acesso restrito)'
    )
    
    version = models.PositiveIntegerField(
        'Versão',
        default=1,
        help_text='Versão do documento'
    )
    
    # ===== OBSERVAÇÕES =====
    notes = models.TextField(
        'Observações',
        blank=True,
        help_text='Anotações sobre o documento'
    )
    
    # Manager customizado
    objects = OrganizationScopedManager()
    
    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organization', 'office']),
            models.Index(fields=['category']),
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Calcula o tamanho do arquivo automaticamente"""
        if self.file and not self.file_size:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
    
    @property
    def file_extension(self):
        """Retorna a extensão do arquivo"""
        if self.file:
            return os.path.splitext(self.file.name)[1].lower()
        return ''
    
    @property
    def file_size_mb(self):
        """Retorna o tamanho em MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0
    
    @property
    def file_icon(self):
        """Retorna ícone baseado na extensão"""
        icons = {
            '.pdf': 'fa-file-pdf',
            '.doc': 'fa-file-word',
            '.docx': 'fa-file-word',
            '.xls': 'fa-file-excel',
            '.xlsx': 'fa-file-excel',
            '.jpg': 'fa-file-image',
            '.jpeg': 'fa-file-image',
            '.png': 'fa-file-image',
            '.zip': 'fa-file-archive',
            '.rar': 'fa-file-archive',
        }
        return icons.get(self.file_extension, 'fa-file')