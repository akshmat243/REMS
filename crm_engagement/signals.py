from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from .models import AgentProfile

@receiver(post_save, sender=User)
def create_agent_profile(sender, instance, created, **kwargs):
    if created and instance.role and instance.role.name.lower() == "agent":
        AgentProfile.objects.create(user=instance)
    elif instance.role and instance.role.name.lower() == "agent":
        AgentProfile.objects.get_or_create(user=instance)
    
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import AgentProfile
from MBP.models import Role   # adjust import to your Role model

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_agent_profile(sender, instance, created, **kwargs):
    """
    Automatically create AgentProfile when a user with role 'Agent' is created
    OR when role changes to Agent later.
    """
    if instance.role and instance.role.name.lower() == "agent":
        AgentProfile.objects.get_or_create(user=instance)
