from .models import *
from .serializers import *
from MBP.views import ProtectedModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

class RequestInfoViewSet(ProtectedModelViewSet):
    queryset = RequestInfo.objects.all()
    serializer_class = RequestInfoSerializer
    model_name = "RequestInfo"
    lookup_field = "slug"

class FeedbackViewSet(ProtectedModelViewSet):
    queryset = Feedback.objects.all().order_by('-submitted_at')
    serializer_class = FeedbackSerializer
    model_name = "Feedback"
    lookup_field = "slug"
    
    @action(detail=False, methods=['get'], url_path='sentiment-summary')
    def sentiment_summary(self, request):
        qs = self.get_queryset()
        return Response({
            'total_feedbacks': qs.count(),
            'positive': qs.filter(ai_sentiment='Positive').count(),
            'neutral': qs.filter(ai_sentiment='Neutral').count(),
            'negative': qs.filter(ai_sentiment='Negative').count(),
        })

class ReportProblemViewSet(ProtectedModelViewSet):
    queryset = ReportProblem.objects.all()
    serializer_class = ReportProblemSerializer
    model_name = "ReportProblem"
    lookup_field = "slug"

class TestimonialViewSet(ProtectedModelViewSet):
    queryset = Testimonial.objects.all().order_by('-submitted_at')
    serializer_class = TestimonialSerializer
    model_name = "Testimonial"
    lookup_field = "slug"

class GrievanceViewSet(ProtectedModelViewSet):
    queryset = Grievance.objects.all().order_by('-created_at')
    serializer_class = GrievanceSerializer
    model_name = "Grievance"
    lookup_field = "slug"
    
    @action(detail=False, methods=['get'], url_path='priority-summary')
    def priority_summary(self, request):
        return Response(
            self.get_queryset().values('ai_priority').annotate(count=Count('id'))
        )

class CustomerServiceLogViewSet(ProtectedModelViewSet):
    queryset = CustomerServiceLog.objects.all()
    serializer_class = CustomerServiceLogSerializer
    model_name = "CustomerServiceLog"
    lookup_field = "slug"

class SummonsNoticeViewSet(ProtectedModelViewSet):
    queryset = SummonsNotice.objects.all()
    serializer_class = SummonsNoticeSerializer
    model_name = "SummonsNotice"
    lookup_field = "slug"

class ChatInteractionLogViewSet(ProtectedModelViewSet):
    queryset = ChatInteractionLog.objects.all().order_by('-timestamp')
    serializer_class = ChatInteractionLogSerializer
    model_name = "ChatInteractionLog"
    lookup_field = "slug"
