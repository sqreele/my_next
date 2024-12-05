from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import RoomViewSet, TopicViewSet, JobViewSet, PropertyViewSet, UserProfileViewSet

# Set the app name correctly
app_name = 'myappLubd'

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

  
    
]
