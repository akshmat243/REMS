from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('request-info', RequestInfoViewSet)
router.register('feedback', FeedbackViewSet)
router.register('report-problems', ReportProblemViewSet)
router.register('testimonials', TestimonialViewSet)
router.register('grievances', GrievanceViewSet)
router.register('service-logs', CustomerServiceLogViewSet)
router.register('summons-notices', SummonsNoticeViewSet)
router.register('chat-logs', ChatInteractionLogViewSet)
router.register('support-tickets', SupportTicketViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
