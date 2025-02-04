from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import RoomViewSet, TopicViewSet, JobViewSet, PropertyViewSet, UserProfileViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CustomSessionView 
from .views import log_view
# Set the app name correctly
app_name = 'myappLubd'

def health_check(request):
    return HttpResponse("OK")

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'user-profiles', UserProfileViewSet)

# Define the URL patterns
urlpatterns = [
    # Include API routes under the 'api/' path
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/session/', CustomSessionView.as_view(), name='auth_session'),
    path('api/auth/_log', log_view, name='log_view'),
      path('api/auth/check/', views.auth_check, name='auth_check'),
    path('health/', health_check, name='health_check'),
    path('api/auth/providers/', views.auth_providers, name='auth_providers'),
    path('api/drf/auth/error/', views.auth_error, name='auth_error'),
    path('api/drf/auth/login/', views.login_view, name='login'),     
    path('api/health/', views.health_check),
  
    
]
