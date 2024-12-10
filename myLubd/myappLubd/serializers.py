from rest_framework import serializers
from .models import Room, Topic, JobImage, Job, Property, UserProfile
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

class JobSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    images = JobImageSerializer(many=True, read_only=True)
    topics = TopicSerializer(many=True, read_only=True)
    profile_image = UserProfileSerializer(source='user.userprofile', read_only=True)
    room_type = serializers.CharField(source='room.room_type', read_only=True)
    name = serializers.CharField(source='room.name', read_only=True)
    rooms = RoomSerializer(many=True, read_only=True)
    
    class Meta:
        model = Job
        fields = ['job_id', 'description', 'status', 'priority', 'created_at', 
                 'updated_at', 'completed_at', 'user', 'profile_image', 
                 'images', 'topics', 'room_type', 'name', 'rooms', 'remarks', 
                 'is_defective']
        read_only_fields = ['job_id', 'created_at', 'updated_at', 'completed_at', 'user']
    def create(self, validated_data):
        # Extract the write-only fields
        topic_data = validated_data.pop('topic_data')
        room_id = validated_data.pop('room_id')
        request = self.context.get('request')
        
        try:
            # Get room
            room = Room.objects.get(room_id=room_id)
            
            # Create or get topic
            topic, _ = Topic.objects.get_or_create(
                title=topic_data['title'],
                defaults={'description': topic_data['description']}
            )

            # Create job
            job = Job.objects.create(
                **validated_data,
                room=room,
                user=request.user
            )
            
            # Add topic to job (since it's a many-to-many relationship)
            job.topics.add(topic)

            # Handle image uploads if they exist
            images = request.FILES.getlist('images')
            for image in images:
                JobImage.objects.create(
                    job=job,
                    image=image
                )

            return job

        except Room.DoesNotExist:
            raise serializers.ValidationError({'room_id': 'Invalid room ID'})
        except KeyError as e:
            raise serializers.ValidationError({
                'topic_data': f'Missing required field: {str(e)}'
            })
        except Exception as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        # This ensures we get full serialized data when retrieving
        representation = super().to_representation(instance)
        return representation