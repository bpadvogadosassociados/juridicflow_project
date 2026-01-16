from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import FeeAgreement, Payment

class PaymentInline(admin.TabularInline):
    """
    Inline para gerenciar pagamentos dentro do contrato.
    """
    model = Payment
    extra = 0
    fields = ['description', 'amount', 'due_date', 'payment_date', 'payment_method', 'status']
    readonly_fields = []

@admin.register(FeeAgreement)
class FeeAgreementAdmin(admin.ModelAdmin):
    """
    Admin para contratos de honorários.
    """
    list_display = [
        'title',
        'customer',
        'type',
        'amount',
        'progress_bar',
        'status_badge',
        'start_date',
        'created_at'
    ]
    
    list_filter = [
        'type',
        'status',
        'organization',
        'office',
        'start_date',
        'created_at'
    ]
    
    search_fields = [
        'title',
        'customer__name',
        'process__number',
        'description'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'installment_amount',
        'total_received',
        'total_pending',
        'percentage_received',
        'is_fully_paid'
    ]
    
    fieldsets = (
        ('Organização', {
            'fields': ('organization', 'office')
        }),
        ('Relacionamentos', {
            'fields': ('customer', 'process')
        }),
        ('Informações Básicas', {
            'fields': ('title', 'type', 'description')
        }),
        ('Valores', {
            'fields': (
                'amount',
                'success_percentage',
                'hourly_rate',
                'installments',
                'installment_amount'
            )
        }),
        ('Período', {
            'fields': ('start_date', 'end_date')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Estatísticas', {
            'fields': (
                'total_received',
                'total_pending',
                'percentage_received',
                'is_fully_paid'
            ),
            'classes': ('collapse',)
        }),
        ('Arquivo', {
            'fields': ('contract_file',),
            'classes': ('collapse',)
        }),
        ('Observações', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    autocomplete_fields = ['customer', 'process']
    
    inlines = [PaymentInline]
    
    actions = ['activate_agreements', 'suspend_agreements']
    
    def status_badge(self, obj):
        """Badge colorido para status"""
        colors = {
            'draft': '#6c757d',
            'active': '#28a745',
            'suspended': '#ffc107',
            'completed': '#0d6efd',
            'cancelled': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def progress_bar(self, obj):
        """Barra de progresso de pagamento"""
        percentage = obj.percentage_received
        color = '#28a745' if percentage >= 100 else '#ffc107' if percentage >= 50 else '#dc3545'
        
        return format_html(
            '<div style="width: 100px; background: #e9ecef; border-radius: 3px; overflow: hidden;">'
            '<div style="width: {}%; background: {}; color: white; text-align: center; padding: 2px; font-size: 10px; font-weight: bold;">'
            '{}%'
            '</div>'
            '</div>',
            min(percentage, 100),
            color,
            int(percentage)
        )
    progress_bar.short_description = 'Progresso'
    
    def activate_agreements(self, request, queryset):
        count = queryset.update(status='active')
        self.message_user(request, f'{count} contrato(s) ativado(s).')
    activate_agreements.short_description = 'Ativar contratos'
    
    def suspend_agreements(self, request, queryset):
        count = queryset.update(status='suspended')
        self.message_user(request, f'{count} contrato(s) suspenso(s).')
    suspend_agreements.short_description = 'Suspender contratos'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin para pagamentos.
    """
    list_display = [
        'description',
        'fee_agreement',
        'amount',
        'due_date',
        'payment_date',
        'status_badge',
        'overdue_badge',
        'payment_method'
    ]
    
    list_filter = [
        'status',
        'payment_method',
        'organization',
        'office',
        'due_date',
        'payment_date'
    ]
    
    search_fields = [
        'description',
        'fee_agreement__title',
        'fee_agreement__customer__name'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'is_overdue',
        'days_overdue'
    ]
    
    fieldsets = (
        ('Organização', {
            'fields': ('organization', 'office')
        }),
        ('Contrato', {
            'fields': ('fee_agreement',)
        }),
        ('Informações', {
            'fields': ('description', 'amount')
        }),
        ('Datas', {
            'fields': ('due_date', 'payment_date')
        }),
        ('Pagamento', {
            'fields': ('payment_method', 'status')
        }),
        ('Comprovante', {
            'fields': ('receipt_file',),
            'classes': ('collapse',)
        }),
        ('Informações Adicionais', {
            'fields': ('is_overdue', 'days_overdue', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Observações', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
    
    autocomplete_fields = ['fee_agreement']
    
    date_hierarchy = 'due_date'
    
    actions = ['mark_as_received', 'mark_as_pending']
    
    def status_badge(self, obj):
        """Badge para status"""
        colors = {
            'pending': '#ffc107',
            'received': '#28a745',
            'cancelled': '#6c757d',
            'refunded': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def overdue_badge(self, obj):
        """Badge de atraso"""
        if not obj.is_overdue:
            return format_html('<span style="color: #28a745;">✓ Em dia</span>')
        
        return format_html(
            '<span style="color: #dc3545; font-weight: bold;">⚠ {} dias</span>',
            obj.days_overdue
        )
    overdue_badge.short_description = 'Atraso'
    
    def mark_as_received(self, request, queryset):
        for payment in queryset:
            payment.mark_as_received()
        count = queryset.count()
        self.message_user(request, f'{count} pagamento(s) marcado(s) como recebido(s).')
    mark_as_received.short_description = 'Marcar como recebido'
    
    def mark_as_pending(self, request, queryset):
        count = queryset.update(status='pending', payment_date=None)
        self.message_user(request, f'{count} pagamento(s) marcado(s) como pendente(s).')
    mark_as_pending.short_description = 'Marcar como pendente'