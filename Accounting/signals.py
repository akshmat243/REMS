from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, Commission
from property.models import Property
from crm_engagement.models import AgentProfile

@receiver(post_save, sender=Transaction)
def update_agent_deals_from_transaction(sender, instance, **kwargs):
    """
    If a transaction is related to a property & has type 'payment' or 'commission',
    then mark the property as sold/rented and update agent's deals count.
    """
    if instance.property and instance.transaction_type in ["payment", "commission"]:
        property_obj = instance.property
        # Auto mark property as sold if transaction successful
        if property_obj.property_status not in ["Sold", "Rented"]:
            property_obj.property_status = "Sold"
            property_obj.save(update_fields=["property_status"])

        if property_obj.agent:
            try:
                agent_profile = property_obj.agent.agent_profile
                closed_deals = Property.objects.filter(
                    agent=property_obj.agent, property_status__in=["Sold", "Rented"]
                ).count()
                agent_profile.deals_closed = closed_deals
                agent_profile.save(update_fields=["deals_closed"])
            except AgentProfile.DoesNotExist:
                pass


@receiver(post_save, sender=Commission)
def update_agent_deals_from_commission(sender, instance, **kwargs):
    """
    When commission entry is created for an agent, recalc closed deals.
    """
    if instance.agent:
        try:
            agent_profile = instance.agent.agent_profile
            closed_deals = Property.objects.filter(
                agent=instance.agent, property_status__in=["Sold", "Rented"]
            ).count()
            agent_profile.deals_closed = closed_deals
            agent_profile.save(update_fields=["deals_closed"])
        except AgentProfile.DoesNotExist:
            pass

from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from property.models import Property
from Accounting.models import Commission, Transaction


@receiver(post_save, sender=Commission)
def update_agent_earnings(sender, instance, **kwargs):
    """
    Update agent's total earnings whenever a commission is recorded.
    """
    if instance.agent:
        try:
            agent_profile = instance.agent.agent_profile
            # ✅ Recalculate total earnings
            total = Commission.objects.filter(agent=instance.agent).aggregate(
                total=Sum("amount")
            )["total"] or 0
            agent_profile.total_earnings = total
            agent_profile.save(update_fields=["total_earnings"])
        except AgentProfile.DoesNotExist:
            pass


@receiver(post_save, sender=Transaction)
def update_agent_deals_and_earnings_from_transaction(sender, instance, **kwargs):
    """
    Handle deals & earnings updates when a transaction is created.
    """
    if instance.property and instance.transaction_type in ["payment", "commission"]:
        property_obj = instance.property
        if property_obj.agent:
            try:
                agent_profile = property_obj.agent.agent_profile

                # ✅ Deals closed logic
                closed_deals = Property.objects.filter(
                    agent=property_obj.agent, property_status__in=["Sold", "Rented"]
                ).count()
                agent_profile.deals_closed = closed_deals

                # ✅ Earnings logic (if transaction type = commission, add amount)
                if instance.transaction_type == "commission":
                    total = Commission.objects.filter(agent=property_obj.agent).aggregate(
                        total=Sum("amount")
                    )["total"] or 0
                    agent_profile.total_earnings = total

                agent_profile.save(update_fields=["deals_closed", "total_earnings"])
            except AgentProfile.DoesNotExist:
                pass
