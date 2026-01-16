# apps/documents/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Admin para gerenciar documentos.
    """
    list_display = [
        'title',
        'category',
        'file_badge',
        'file_size_display',
        'uploaded_by',
        'is_confidential',
        'created_at'
    ]
    
    list_filter = [
        'category',
        'is_confidential',
        'organization',
        'office',
        'uploaded_by',
        'created_at'
    ]
    
    search_fields = [
        'title',
        'description',
        'file'
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'file_size',
        'file_extension',
        'file_size_mb',
        'uploaded_by'
    ]
    
    fieldsets = (
        ('Organização', {
            'fields': ('organization', 'office')
        }),
        ('Informações Básicas', {
            'fields': ('title', 'category', 'description')
        }),
        ('Arquivo', {
            'fields': ('file', 'file_size', 'file_extension', 'file_size_mb', 'version')
        }),
        ('Vinculação', {
            'fields': ('content_type', 'object_id'),
            'classes': ('collapse',),
            'description': 'Vincular a um processo, cliente, etc.'
        }),
        ('Controle', {
            'fields': ('uploaded_by', 'is_confidential')
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
    
    def save_model(self, request, obj, form, change):
        """Auto-preenche uploaded_by"""
        if not obj.pk:  # Se é novo
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)
    
    def file_badge(self, obj):
        """Badge com ícone do tipo de arquivo"""
        icon = obj.file_icon
        ext = obj.file_extension.upper().replace('.', '')
        
        colors = {
            'PDF': '#dc3545',
            'DOC': '#0d6efd',
            'DOCX': '#0d6efd',
            'XLS': '#198754',
            'XLSX': '#198754',
            'JPG': '#fd7e14',
            'JPEG': '#fd7e14',
            'PNG': '#fd7e14',
        }
        color = colors.get(ext, '#6c757d')
        
        return format_html(
            '<i class="fas {} " style="color: {}"></i> {}',
            icon,
            color,
            ext if ext else 'FILE'
        )
    file_badge.short_description = 'Tipo'
    
    def file_size_display(self, obj):
        """Exibe tamanho do arquivo formatado"""
        if obj.file_size:
            if obj.file_size < 1024:
                return f'{obj.file_size} B'
            elif obj.file_size < 1024 * 1024:
                return f'{obj.file_size / 1024:.1f} KB'
            else:
                return f'{obj.file_size_mb} MB'
        return '-'
    file_size_display.short_description = 'Tamanho'