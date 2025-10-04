from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("agents", AgentProfileViewSet, basename="agent")
router.register(r"agent-reviews", AgentReviewViewSet, basename="agent-review")
router.register('leads', LeadViewSet)
router.register('interactions', InteractionLogViewSet)
router.register('notifications', NotificationViewSet)
router.register('wishlist', WishlistViewSet)
router.register('comparisons', PropertyComparisonViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
