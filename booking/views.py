from .models import VisitRequest, Appointment, RentAgreement
from .serializers import *
from MBP.views import ProtectedModelViewSet
from rest_framework.decorators import action

class VisitRequestViewSet(ProtectedModelViewSet):
    queryset = VisitRequest.objects.all().order_by('-created_at')
    serializer_class = VisitRequestSerializer
    model_name = "VisitRequest"
    lookup_field = "slug"
    
    @action(detail=False, methods=['get'], url_path='most-visited')
    def most_visited(self, request):
        data = self.get_queryset().values('property__title').annotate(visits=Count('id')).order_by('-visits')[:5]
        return Response(data)

class AppointmentViewSet(ProtectedModelViewSet):
    queryset = Appointment.objects.all().order_by('-appointment_time')
    serializer_class = AppointmentSerializer
    model_name = "Appointment"
    lookup_field = "slug"

class RentAgreementViewSet(ProtectedModelViewSet):
    queryset = RentAgreement.objects.all().order_by('-agreement_start')
    serializer_class = RentAgreementSerializer
    model_name = "RentAgreement"
    lookup_field = "slug"

