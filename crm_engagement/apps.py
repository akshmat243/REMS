from django.apps import AppConfig


class CrmEngagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crm_engagement'

    def ready(self):
        import crm_engagement.signals