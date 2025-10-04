from .models import *
from .serializers import *
from MBP.views import ProtectedModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

class AgentProfileViewSet(ProtectedModelViewSet):
    queryset = AgentProfile.objects.select_related("user").all()
    serializer_class = AgentProfileSerializer
    model_name = "AgentProfile"
    lookup_field = "slug"
    
    @action(detail=True, methods=["get"], url_path="profile", permission_classes=[AllowAny])
    def profile_detail(self, request, slug=None):
        """
        Public API: Get detailed agent profile with reviews.
        Example: /api/agents/{slug}/profile/
        """
        agent = self.get_object()
        serializer = AgentProfileSerializer(agent, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="top", permission_classes=[AllowAny])
    def top_agents(self, request):
        """
        Public API: Show top agents (verified, most deals, best ratings).
        """
        agents = (
            AgentProfile.objects.filter(verified=True)
            .order_by("-deals_closed", "-rating")[:6]
        )
        serializer = self.get_serializer(agents, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="verify", permission_classes=[])
    def verify_agent(self, request, pk=None):
        """
        Admin action: Verify an agent.
        """
        agent = self.get_object()
        if not request.user.is_superuser:
            return Response({"error": "Not authorized"}, status=403)
        agent.verified = True
        agent.save()
        return Response({"message": f"Agent {agent.user.full_name} verified"})
    
    @action(detail=False, methods=["get"], url_path="leaderboard", permission_classes=[AllowAny])
    def leaderboard(self, request):
        """
        Public API: Returns leaderboard of agents ranked by earnings, deals, and rating.
        Example: /api/agents/leaderboard/
        """
        # Top 5 by earnings
        top_by_earnings = AgentProfile.objects.order_by("-total_earnings")[:5]

        # Top 5 by deals
        top_by_deals = AgentProfile.objects.order_by("-deals_closed")[:5]

        # Top 5 by rating
        top_by_rating = AgentProfile.objects.order_by("-rating", "-total_reviews")[:5]

        data = {
            "top_by_earnings": AgentProfileSerializer(top_by_earnings, many=True).data,
            "top_by_deals": AgentProfileSerializer(top_by_deals, many=True).data,
            "top_by_rating": AgentProfileSerializer(top_by_rating, many=True).data,
        }
        return Response(data)

class AgentReviewViewSet(ProtectedModelViewSet):
    queryset = AgentReview.objects.all()
    serializer_class = AgentReviewSerializer
    lookup_field = "id"
    model_name = "AgentReview"  # ✅ for role-based permission system

    def get_permissions(self):
        """
        Override permissions: 
        - Public can list reviews
        - Only authenticated can create
        """
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """
        Authenticated users can add a review for an agent.
        The user is set automatically from the logged-in account.
        """
        serializer = AgentReviewCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(user=request.user)  # ✅ secure: prevent spoofing
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def by_agent(self, request):
        """
        Public API: Fetch all reviews for a given agent.
        Example: /api/agent-reviews/by_agent/?agent_slug=xyz
        """
        agent_slug = request.GET.get("agent_slug")
        if not agent_slug:
            return Response({"error": "agent_slug is required"}, status=status.HTTP_400_BAD_REQUEST)

        reviews = AgentReview.objects.filter(agent__slug=agent_slug).order_by("-created_at")
        serializer = AgentReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LeadViewSet(ProtectedModelViewSet):
    queryset = Lead.objects.all().order_by('-id')
    serializer_class = LeadSerializer
    model_name = "Lead"
    lookup_field = "slug"
    
    @action(detail=False, methods=['get'], url_path='conversion-rate')
    def conversion_rate(self, request):
        total = self.get_queryset().count()
        converted = self.get_queryset().filter(status__iexact="Converted").count()
        rate = round((converted / total) * 100, 2) if total else 0
        return Response({
            "total_leads": total,
            "converted": converted,
            "conversion_rate_percent": rate
        })


class InteractionLogViewSet(ProtectedModelViewSet):
    queryset = InteractionLog.objects.all().order_by('-date')
    serializer_class = InteractionLogSerializer
    model_name = "InteractionLog"
    lookup_field = "slug"


class NotificationViewSet(ProtectedModelViewSet):
    queryset = Notification.objects.all().order_by('-id')
    serializer_class = NotificationSerializer
    model_name = "Notification"
    lookup_field = "slug"


class WishlistViewSet(ProtectedModelViewSet):
    queryset = Wishlist.objects.all().select_related("property", "user").order_by('-added_at')
    serializer_class = WishlistSerializer
    model_name = "Wishlist"
    lookup_field = "slug"


class PropertyComparisonViewSet(ProtectedModelViewSet):
    queryset = PropertyComparison.objects.all().order_by('-compared_at')
    serializer_class = PropertyComparisonSerializer
    model_name = "PropertyComparison"
    lookup_field = "slug"
