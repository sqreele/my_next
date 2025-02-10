from rest_framework import serializers
from .models import Room, Topic, JobImage, Job, Property, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
        
            'name',
            'description',
            'property_id',
            'users',
            'created_at',
         
          
        
        ]
        read_only_fields = ['created_at']

class UserProfileSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True, read_only=True)
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'profile_image',
            'positions',
            'properties',
           
        ]
    def get_username(self, obj):
        return obj.user.username    
      

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    class Meta:
        model = Property
        fields = '__all__'

# Keep only this version of JobImageSerializer
class JobImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = JobImage
        fields = ['id', 'image_url', 'uploaded_by', 'uploaded_at']

    def get_image_url(self, obj):
        """
        Return the absolute URL for the WebP image.
        """
        if obj.image:
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['title', 'description','id']
from django.db import transaction
class JobSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    images = JobImageSerializer(source='job_images', many=True, read_only=True)  # Use job_images
    topics = TopicSerializer(many=True, read_only=True)
    profile_image = UserProfileSerializer(source='user.userprofile', read_only=True)
    room_type = serializers.CharField(source='room.room_type', read_only=True)
    name = serializers.CharField(source='room.name', read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    topic_data = serializers.JSONField(write_only=True)
    room_id = serializers.IntegerField(write_only=True)
    image_urls = serializers.SerializerMethodField()
   
    class Meta:
        model = Job
        fields = [
            'job_id', 'description', 'status', 'priority',
            'created_at', 'updated_at', 'completed_at',
            'user', 'profile_image', 'images', 'topics',
            'room_type', 'name', 'rooms', 'remarks',
            'is_defective', 'topic_data', 'room_id',
            'image_urls','id'
        ]
        read_only_fields = ['job_id', 'created_at', 'updated_at', 'completed_at', 'user']

    def get_image_urls(self, obj):
        """Return a list of full URLs for all images associated with the job"""
        request = self.context.get('request')
        if request and obj.job_images.exists():  # Use job_images
            return [
                request.build_absolute_uri(image.image.url)
                for image in obj.job_images.all()  # Use job_images
            ]
        return []

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("User must be logged in to create a job")

        topic_data = validated_data.pop('topic_data', None)
        room_id = validated_data.pop('room_id', None)

        if not room_id:
            raise serializers.ValidationError({'room_id': 'This field is required.'})
        if not topic_data or 'title' not in topic_data:
            raise serializers.ValidationError({'topic_data': 'This field is required and must include a title.'})

        try:
            with transaction.atomic():
                # Get the room
                room = Room.objects.get(room_id=room_id)

                # Create or get topic
                topic, _ = Topic.objects.get_or_create(
                    title=topic_data['title'],
                    defaults={'description': topic_data.get('description', '')}
                )

                # Create job
                job = Job.objects.create(
                    **validated_data,
                    user=request.user
                )

                # Add relationships
                job.rooms.add(room)
                job.topics.add(topic)

                # Handle images
                images = request.FILES.getlist('images', [])
                for image in images:
                    JobImage.objects.create(
                        job=job,
                        image=image,
                        uploaded_by=request.user
                    )

                job.refresh_from_db()
                return job

        except Room.DoesNotExist:
            raise serializers.ValidationError({'room_id': 'Invalid room ID'})
        except Exception as e:
            raise serializers.ValidationError({'detail': str(e)})




def to_representation(self, instance):
    data = super().to_representation(instance)
    print("Response data:", data)  # Debug line
    return data
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        
        # Validate username
        username = attrs.get('username', '')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": "A user with that username already exists."}
            )
        
        # Validate email
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "A user with that email already exists."}
            )
            
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Create associated UserProfile
        UserProfile.objects.create(
            user=user,
            email=validated_data['email']
        )
        
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError(
                "Both username and password are required."
            )

        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            'id', 
            'username', 
            'email', 
            'profile_image',
            'positions',
            'properties'
        )
        read_only_fields = ('id',)
