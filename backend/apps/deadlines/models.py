# apps/deadlines/models.py

from django.db import models
from apps.shared.models import OrganizationScopedModel
from apps.shared.managers import OrganizationScopedManager
from apps.accounts.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Deadline(OrganizationScopedModel):
    """
    Prazo ou compromisso.
    Pode estar vinculado a processo, contrato, tarefa, etc.
    """
    
    TYPE_CHOICES = [
        ('legal', 'Prazo Legal'),
        ('hearing', 'Audiência'),
        ('meeting', 'Reunião'),
        ('task', 'Tarefa'),
        ('other', 'Outro'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Baixa'),
        ('medium', 'Média'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('in_progress', 'Em Andamento'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
        ('overdue', 'Atrasado'),
    ]
    
    # ===== INFORMAÇÕES BÁSICAS =====
    title = models.CharField(
        'Título',
        max_length=255,
        help_text='Descrição curta do prazo'
    )
    
    description = models.TextField(
        'Descrição',
        blank=True,
        help_text='Detalhes do prazo ou compromisso'
    )
    
    type = models.CharField(
        'Tipo',
        max_length=20,
        choices=TYPE_CHOICES,
        default='task'
    )
    
    # ===== DATAS =====
    due_date = models.DateField(
        'Data de Vencimento',
        help_text='Data limite do prazo'
    )
    
    due_time = models.TimeField(
        'Horário',
        null=True,
        blank=True,
        help_text='Horário específico (opcional)'
    )
    
    completed_at = models.DateTimeField(
        'Concluído em',
        null=True,
        blank=True
    )
    
    # ===== PRIORIDADE E STATUS =====
    priority = models.CharField(
        'Prioridade',
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium'
    )
    
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # ===== RESPONSÁVEL =====
    responsible = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deadlines',
        verbose_name='Responsável',
        help_text='Usuário responsável por este prazo'
    )
    
    # ===== VINCULAÇÃO GENÉRICA =====
    # Permite vincular a Process, Contract, ou qualquer outro model
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
    
    # ===== ALERTAS =====
    alert_days_before = models.IntegerField(
        'Alertar quantos dias antes',
        default=3,
        help_text='Quantidade de dias antes para enviar alerta'
    )
    
    alert_sent = models.BooleanField(
        'Alerta Enviado',
        default=False,
        help_text='Se o alerta já foi enviado'
    )
    
    # ===== OBSERVAÇÕES =====
    notes = models.TextField(
        'Observações',
        blank=True,
        help_text='Anotações internas'
    )
    
    # Manager customizado
    objects = OrganizationScopedManager()
    
    class Meta:
        verbose_name = 'Prazo'
        verbose_name_plural = 'Prazos'
        ordering = ['due_date', 'due_time']
        indexes = [
            models.Index(fields=['organization', 'office']),
            models.Index(fields=['due_date']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['responsible']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.due_date}"
    
    @property
    def is_overdue(self):
        """Verifica se o prazo está atrasado"""
        from django.utils import timezone
        if not self.due_date:
            return False

        if self.status in ['completed', 'cancelled']:
            return False
        return timezone.now().date() > self.due_date
    
    @property
    def days_remaining(self):
        """Retorna quantos dias faltam"""
        from django.utils import timezone
        if not self.due_date:
            return None

        if self.status in ['completed', 'cancelled']:
            return None
        delta = self.due_date - timezone.now().date()
        return delta.days
    
    def mark_as_completed(self):
        """Marca como concluído"""
        from django.utils import timezone
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
    
    def save(self, *args, **kwargs):
        """Auto-atualiza status para atrasado se necessário"""
        if self.is_overdue and self.status == 'pending':
            self.status = 'overdue'
        super().save(*args, **kwargs)