
from django.contrib import admin
from .models import Room, Topic, JobImage, Job, Property

from .models import UserProfile
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type', 'is_active', 'created_at')
    list_filter = ('room_type', 'is_active')
    search_fields = ('name',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

@admin.register(JobImage)
class JobImageAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_uploaded_by', 'get_uploaded_at')
    list_filter = (('uploaded_at', admin.DateFieldListFilter),)  # Fixed list_filter
    search_fields = ('name', 'description')
    readonly_fields = ('get_uploaded_at',)  # Fixed readonly_fields

    def get_name(self, obj):
        return obj.name
    get_name.short_description = 'Name'
    
    def get_uploaded_by(self, obj):
        return obj.uploaded_by
    get_uploaded_by.short_description = 'Uploaded By'
    
    def get_uploaded_at(self, obj):
        return obj.uploaded_at
    get_uploaded_at.short_description = 'Upload Date'

# Register other models

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'user', 'status', 'priority','remarks', 'created_at', 'completed_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('job_id', 'description')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_id', 'created_at')
    search_fields = ('name', 'property_id')
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'positions', 'profile_image_tag')  # Use profile_image_tag here
    search_fields = ('user__username',)
    list_filter = ('user__is_active',)

    # Method to display image in admin
    def profile_image_tag(self, obj):
        if obj.profile_image:
            return f'<img src="{obj.profile_image.url}" width="50" height="50" />'
        return "No Image"
    profile_image_tag.short_description = 'Profile Image'
    profile_image_tag.allow_tags = True