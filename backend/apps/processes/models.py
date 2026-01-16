from django.db import models
from apps.shared.models import OrganizationScopedModel
from apps.shared.managers import OrganizationScopedManager
from apps.customers.models import Customer

class Process(OrganizationScopedModel):

    """
    Processo judicial.
    Número CNJ, tribunal, fase, etc.
    """
    
    PHASE_CHOICES = [
        ('initial', 'Inicial'),
        ('instruction', 'Instrução'),
        ('sentence', 'Sentença'),
        ('appeal', 'Recurso'),
        ('execution', 'Execução'),
        ('archived', 'Arquivado'),
    ]
    
    AREA_CHOICES = [
        ('civil', 'Cível'),
        ('criminal', 'Criminal'),
        ('labor', 'Trabalhista'),
        ('family', 'Família'),
        ('tax', 'Tributário'),
        ('administrative', 'Administrativo'),
        ('other', 'Outro'),
    ]
    
    # ===== IDENTIFICAÇÃO =====
    number = models.CharField(
        'Número CNJ',
        max_length=25,
        unique=True,
        help_text='Número único do processo (formato CNJ: NNNNNNN-DD.AAAA.J.TR.OOOO)'
    )
    
    internal_number = models.CharField(
        'Número Interno',
        max_length=50,
        blank=True,
        help_text='Número de controle interno do escritório'
    )
    
    # ===== CLASSIFICAÇÃO =====
    area = models.CharField(
        'Área',
        max_length=20,
        choices=AREA_CHOICES,
        default='civil'
    )
    
    subject = models.CharField(
        'Assunto',
        max_length=255,
        help_text='Assunto principal do processo'
    )
    
    # ===== TRIBUNAL =====
    court = models.CharField(
        'Tribunal',
        max_length=255,
        help_text='Nome do tribunal (ex: TJSP, STJ, etc)'
    )
    
    court_division = models.CharField(
        'Vara/Câmara',
        max_length=255,
        blank=True,
        help_text='Vara ou Câmara'
    )
    
    # ===== FASE PROCESSUAL =====
    phase = models.CharField(
        'Fase',
        max_length=20,
        choices=PHASE_CHOICES,
        default='initial'
    )
    
    # ===== VALOR DA CAUSA =====
    value = models.DecimalField(
        'Valor da Causa',
        max_digits=15,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Valor da causa em R$'
    )
    
    # ===== DATAS =====
    distribution_date = models.DateField(
        'Data de Distribuição',
        null=True,
        blank=True,
        help_text='Data em que o processo foi distribuído'
    )
    
    # ===== OBSERVAÇÕES =====
    notes = models.TextField(
        'Observações',
        blank=True,
        help_text='Anotações internas sobre o processo'
    )
    
    # ===== STATUS =====
    is_active = models.BooleanField(
        'Ativo',
        default=True,
        help_text='Processo ativo'
    )
    
    is_confidential = models.BooleanField(
        'Confidencial',
        default=False,
        help_text='Processo com segredo de justiça'
    )
    
    # Manager customizado
    objects = OrganizationScopedManager()
    
    class Meta:
        verbose_name = 'Processo'
        verbose_name_plural = 'Processos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['organization', 'office']),
            models.Index(fields=['number']),
            models.Index(fields=['phase']),
            models.Index(fields=['area']),
        ]
    
    def __str__(self):
        return f"{self.number} - {self.subject}"
    
    @property
    def parties_count(self):
        """Retorna quantidade de partes no processo"""
        return self.parties.count()

    @property
    def deadlines_count(self):
        """Retorna quantidade de prazos vinculados ao processo"""
        from apps.deadlines.models import Deadline
        from django.contrib.contenttypes.models import ContentType
        ct = ContentType.objects.get_for_model(self)
        return Deadline.objects.filter(
            content_type=ct,
            object_id=self.id
        ).count()


class ProcessParty(models.Model):
    """
    Relacionamento entre Process e Customer.
    Define o papel de cada parte no processo (autor, réu, etc).
    """
    
    ROLE_CHOICES = [
        ('plaintiff', 'Autor'),
        ('defendant', 'Réu'),
        ('third_party', 'Terceiro'),
        ('witness', 'Testemunha'),
        ('expert', 'Perito'),
        ('lawyer', 'Advogado da Parte Contrária'),
    ]
    
    process = models.ForeignKey(
        Process,
        on_delete=models.CASCADE,
        related_name='parties',
        verbose_name='Processo'
    )
    
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='process_parties',
        verbose_name='Cliente'
    )
    
    role = models.CharField(
        'Papel',
        max_length=20,
        choices=ROLE_CHOICES,
        help_text='Papel da parte no processo'
    )
    
    notes = models.TextField(
        'Observações',
        blank=True,
        help_text='Observações sobre esta parte'
    )
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Parte do Processo'
        verbose_name_plural = 'Partes do Processo'
        # Não pode adicionar a mesma pessoa 2x com o mesmo papel
        unique_together = [['process', 'customer', 'role']]
    
    def __str__(self):
        return f"{self.customer.name} - {self.get_role_display()}"