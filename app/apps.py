from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = 'Raj Cafe Application'
    
    def ready(self):
        # Import signals if any
        # import app.signals
        pass