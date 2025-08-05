from .models import PriceTrend, InvestmentOpportunity
from .serializers import *
from MBP.views import ProtectedModelViewSet

class PriceTrendViewSet(ProtectedModelViewSet):
    queryset = PriceTrend.objects.all().order_by('-trend_date')
    serializer_class = PriceTrendSerializer
    model_name = "PriceTrend"
    lookup_field = "slug"


class InvestmentOpportunityViewSet(ProtectedModelViewSet):
    queryset = InvestmentOpportunity.objects.all().order_by('-id')
    serializer_class = InvestmentOpportunitySerializer
    model_name = "InvestmentOpportunity"
    lookup_field = "slug"
