from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
import json
from django.shortcuts import get_object_or_404
from .models import Room, Topic, Job, Property, UserProfile
from .serializers import (
    RoomSerializer, 
    TopicSerializer, 
    JobSerializer, 
    PropertySerializer,
    UserProfileSerializer
)
import logging

logger = logging.getLogger(__name__)

class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class TopicViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class JobViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'job_id'  # Use job_id instead of pk for lookups

    def get_object(self):
        """
        Override get_object to use job_id for lookups
        """
        queryset = self.get_queryset()
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True, methods=['patch'])
    def update_status(self, request, job_id=None):
        """
        Custom action to update job status
        """
        job = self.get_object()
        status_value = request.data.get('status')
        
        if status_value and status_value not in dict(Job.STATUS_CHOICES):
            return Response(
                {"detail": "Invalid status value."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        job.status = status_value
        job.save()
        serializer = self.get_serializer(job)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to add custom logging
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            logger.info(f"Retrieved job: {instance.job_id}")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving job: {str(e)}")
            return Response(
                {"detail": "Job not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class PropertyViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer