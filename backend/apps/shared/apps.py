from django.apps import AppConfig

class SharedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.shared'
    verbose_name = 'Compartilhado'
    
    def ready(self):
        """Importa signals quando o app está pronto"""
        import apps.shared.signals  # ← Adicionar