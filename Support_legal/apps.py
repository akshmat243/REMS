from django.apps import AppConfig


class SupportLegalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Support_legal'

    def ready(self):
        import Support_legal.signals