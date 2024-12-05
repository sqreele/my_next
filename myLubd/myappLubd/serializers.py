from rest_framework import serializers
from .models import Room, Topic, JobImage, Job, Property,UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'positions', 'username', 'properties']
        extra_kwargs = {
            'positions': {'required': False},
            'properties': {'required': False}
        }
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = '__all__'
class JobImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobImage
        fields = ['image', 'name', 'description', 'uploaded_by', 'uploaded_at']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['title', 'description']

class JobSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    images = JobImageSerializer(many=True)
    topics = TopicSerializer(many=True)
    profile_image = UserProfileSerializer(source='user.userprofile', read_only=True)
    room_type = serializers.CharField(source='room.room_type', read_only=True)  # Add this line
    name = serializers.CharField(source='room.name', read_only=True)
    rooms = RoomSerializer(many=True, read_only=True) # Add this line if you want the room name

    class Meta:
        model = Job
        fields = ['job_id', 'description', 'status', 'priority', 'created_at', 
                 'updated_at', 'completed_at', 'user', 'profile_image', 
                 'images', 'topics', 'room_type', 'name', 'rooms','remarks'] 
        
class JobImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    original_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = JobImage
        fields = ['id', 'image_url', 'original_image_url', 'name', 
                 'description', 'uploaded_by', 'uploaded_at']

    def get_image_url(self, obj):
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

    def get_original_image_url(self, obj):
        if obj.original_image:
            return self.context['request'].build_absolute_uri(obj.original_image.url)
        return None        
        
        
        