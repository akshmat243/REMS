from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LogoutView, LoginView, RegisterView, GoogleLogin
from django.urls import path, include

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/login/', LoginView.as_view(), name='login'),
    path("api/auth/google/", GoogleLogin.as_view(), name="google_login"),

]


# Create user via POST /api/users/

# Update user via PUT/PATCH /api/users/{id}/

# Assign role via POST /api/users/{id}/assign-role/