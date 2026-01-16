from django.db import models

class Organization(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]

    name = models.CharField('nome' ,max_length=255, help_text="Nome da Empresa")
    document = models.CharField('CNPJ', max_length=18, unique=True, help_text="CNPJ or CPF")
    plan = models.CharField('Plano', max_length=20, choices=PLAN_CHOICES, default='free')
    is_active = models.BooleanField('ativo', default=True, help_text="Indica se a organização está ativa")

    # JSON para configurações flexiveis
    settings = models.JSONField('configurações', default=dict, blank=True, help_text="Configurações adicionais da organização")

    # Dates
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Organização'
        verbose_name_plural = 'Organizações'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def total_offices(self):
        return self.offices.count()

    @property
    def total_users(self):

        return self.memberships.values('user').distinct().count()
