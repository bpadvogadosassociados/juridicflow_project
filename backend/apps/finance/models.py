from django.db import models
from apps.shared.models import OrganizationScopedModel
from apps.shared.managers import OrganizationScopedManager
from apps.customers.models import Customer
from apps.processes.models import Process
from decimal import Decimal

class FeeAgreement(OrganizationScopedModel):
    """
    Contrato de honorários com cliente.
    Define como e quanto o cliente vai pagar.
    """
    
    TYPE_CHOICES = [
        ('fixed', 'Valor Fixo'),
        ('hourly', 'Por Hora'),
        ('success', 'Por Êxito'),
        ('monthly', 'Mensalidade'),
        ('percentage', 'Percentual'),
        ('hybrid', 'Híbrido'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('active', 'Ativo'),
        ('suspended', 'Suspenso'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
    ]
    
    # ===== RELACIONAMENTOS =====
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='fee_agreements',
        verbose_name='Cliente'
    )
    
    process = models.ForeignKey(
        Process,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fee_agreements',
        verbose_name='Processo',
        help_text='Processo vinculado (opcional)'
    )
    
    # ===== INFORMAÇÕES BÁSICAS =====
    title = models.CharField(
        'Título',
        max_length=255,
        help_text='Ex: Contrato de Honorários - Ação Trabalhista'
    )
    
    type = models.CharField(
        'Tipo',
        max_length=20,
        choices=TYPE_CHOICES,
        default='fixed'
    )
    
    description = models.TextField(
        'Descrição',
        blank=True,
        help_text='Detalhes do contrato'
    )
    
    # ===== VALORES =====
    amount = models.DecimalField(
        'Valor',
        max_digits=15,
        decimal_places=2,
        help_text='Valor do honorário em R$'
    )
    
    success_percentage = models.DecimalField(
        'Percentual Êxito',
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Percentual sobre o valor obtido (para êxito)'
    )
    
    hourly_rate = models.DecimalField(
        'Valor Hora',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Valor por hora trabalhada'
    )
    
    # ===== PARCELAMENTO =====
    installments = models.PositiveIntegerField(
        'Parcelas',
        default=1,
        help_text='Quantidade de parcelas'
    )
    
    installment_amount = models.DecimalField(
        'Valor da Parcela',
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Valor de cada parcela (calculado automaticamente)'
    )
    
    # ===== DATAS =====
    start_date = models.DateField(
        'Data de Início',
        help_text='Data de início do contrato'
    )
    
    end_date = models.DateField(
        'Data de Término',
        null=True,
        blank=True,
        help_text='Data de término (opcional)'
    )
    
    # ===== STATUS =====
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )
    
    # ===== OBSERVAÇÕES =====
    notes = models.TextField(
        'Observações',
        blank=True,
        help_text='Anotações internas'
    )
    
    # ===== ARQUIVOS =====
    contract_file = models.FileField(
        'Arquivo do Contrato',
        upload_to='contracts/%Y/%m/',
        null=True,
        blank=True,
        help_text='PDF do contrato assinado'
    )
    
    # Manager customizado
    objects = OrganizationScopedManager()
    
    class Meta:
        verbose_name = 'Contrato de Honorários'
        verbose_name_plural = 'Contratos de Honorários'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organization', 'office']),
            models.Index(fields=['customer']),
            models.Index(fields=['status']),
            models.Index(fields=['start_date']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.customer.name}"
    
    def save(self, *args, **kwargs):
        """Calcula valor da parcela automaticamente"""
        if self.amount and self.installments:
            self.installment_amount = self.amount / Decimal(self.installments)
        super().save(*args, **kwargs)
    
    @property
    def total_received(self):
        """Total já recebido"""
        from apps.finance.models import Payment
        return Payment.objects.filter(
            fee_agreement=self,
            status='received'
        ).aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')
    
    @property
    def total_pending(self):
        """Total ainda pendente"""
        return self.amount - self.total_received
    
    @property
    def percentage_received(self):
        """Percentual recebido"""
        if not self.amount:
            return False

        if self.amount > 0:
            return (self.total_received / self.amount) * 100
        return 0
    
    @property
    def is_fully_paid(self):
        """Verifica se está totalmente pago"""
        return self.total_received >= self.amount
    
    
class Payment(OrganizationScopedModel):
    """
    Registro de pagamento de honorários.
    """
    
    METHOD_CHOICES = [
        ('cash', 'Dinheiro'),
        ('debit', 'Débito'),
        ('credit', 'Crédito'),
        ('pix', 'PIX'),
        ('bank_transfer', 'Transferência Bancária'),
        ('check', 'Cheque'),
        ('other', 'Outro'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('received', 'Recebido'),
        ('cancelled', 'Cancelado'),
        ('refunded', 'Estornado'),
    ]
    
    # ===== RELACIONAMENTOS =====
    fee_agreement = models.ForeignKey(
        FeeAgreement,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Contrato'
    )
    
    # ===== INFORMAÇÕES =====
    description = models.CharField(
        'Descrição',
        max_length=255,
        help_text='Ex: Parcela 1/12, Honorário Inicial, etc'
    )
    
    amount = models.DecimalField(
        'Valor',
        max_digits=15,
        decimal_places=2,
        help_text='Valor do pagamento em R$'
    )
    
    # ===== DATAS =====
    due_date = models.DateField(
        'Data de Vencimento',
        help_text='Data de vencimento do pagamento'
    )
    
    payment_date = models.DateField(
        'Data de Pagamento',
        null=True,
        blank=True,
        help_text='Data em que foi efetivamente pago'
    )
    
    # ===== MÉTODO E STATUS =====
    payment_method = models.CharField(
        'Forma de Pagamento',
        max_length=20,
        choices=METHOD_CHOICES,
        default='pix'
    )
    
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # ===== COMPROVANTE =====
    receipt_file = models.FileField(
        'Comprovante',
        upload_to='receipts/%Y/%m/',
        null=True,
        blank=True,
        help_text='Comprovante de pagamento'
    )
    
    # ===== OBSERVAÇÕES =====
    notes = models.TextField(
        'Observações',
        blank=True
    )
    
    # Manager customizado
    objects = OrganizationScopedManager()
    
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['due_date']
        indexes = [
            models.Index(fields=['organization', 'office']),
            models.Index(fields=['fee_agreement']),
            models.Index(fields=['status']),
            models.Index(fields=['due_date']),
        ]
    
    def __str__(self):
        return f"{self.description} - R$ {self.amount}"
    
    @property
    def is_overdue(self):
        """Verifica se está atrasado"""
        from django.utils import timezone

        if not self.due_date:
            return False

        if self.status in ['received', 'cancelled', 'refunded']:
            return False
        return timezone.now().date() > self.due_date
    
    @property
    def days_overdue(self):
        """Dias de atraso"""
        from django.utils import timezone
        if not self.is_overdue:
            return 0
        delta = timezone.now().date() - self.due_date
        return delta.days
    
    def mark_as_received(self, payment_date=None):
        """Marca como recebido"""
        from django.utils import timezone
        self.status = 'received'
        self.payment_date = payment_date or timezone.now().date()
        self.save()