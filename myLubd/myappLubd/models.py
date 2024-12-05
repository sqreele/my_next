from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
import os
from django.core.files.base import ContentFile
from pathlib import Path

def get_upload_path(instance, filename):
    """Generate a unique path for uploaded files"""
    ext = Path(filename).suffix
    random_filename = get_random_string(length=12)
    return f'maintenance_job_images/{timezone.now().strftime("%Y/%m")}/{random_filename}{ext}'

class ImageProcessor:
    @staticmethod
    def process_image(image, max_width=200, max_height=100, quality=85):
        """Process and optimize images"""
        if not image:
            return None
            
        img = Image.open(image)
        
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        aspect = img.width / img.height
        new_width = min(max_width, img.width)
        new_height = min(max_height, int(new_width / aspect))
        
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        output = BytesIO()
        img.save(output, format='WEBP', quality=quality, optimize=True)
        output.seek(0)
        
        return output

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    room_type = models.CharField(max_length=50, db_index=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['room_type', 'name']
        verbose_name_plural = 'Rooms'
        indexes = [
            models.Index(fields=['room_type']),
            models.Index(fields=['is_active'])
        ]

    def __str__(self):
        return f"{self.room_type} - {self.name}"

    def clean(self):
        self.name = self.name.strip()
        if not self.name:
            raise ValidationError("Room name cannot be empty.")

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()

class Topic(models.Model):
    title = models.CharField(
        max_length=160, 
        unique=True, 
        verbose_name="Subject"
    )
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Topics'

    def __str__(self):
        return self.title

class JobImage(models.Model):
    original_image = models.ImageField(
        upload_to=get_upload_path,
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'webp'])],
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='maintenance_job_images/%Y/%m/webp/',
        null=True,
        blank=True
    )
    description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='uploaded_job_images'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = 'Job Images'
        app_label = 'myappLubd'

    def __str__(self):
        return f"{self.name} (Uploaded: {self.uploaded_at.date()})"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        if is_new and self.original_image:
            super().save(*args, **kwargs)
            
            try:
                processed = ImageProcessor.process_image(self.original_image)
                if processed:
                    name = Path(self.original_image.name).stem
                    webp_name = f'{name}.webp'
                    
                    self.image.save(
                        webp_name,
                        ContentFile(processed.getvalue()),
                        save=False
                    )
                    
                    processed.close()
            except Exception as e:
                print(f"Error processing image: {e}")
                
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.original_image:
            if os.path.isfile(self.original_image.path):
                os.remove(self.original_image.path)
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

class Job(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('waiting_sparepart', 'Waiting Sparepart'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ]
   
    job_id = models.CharField(
        max_length=16, 
        unique=True, 
        blank=True, 
        editable=False
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='maintenance_jobs'
    )
    rooms = models.ManyToManyField(
        Room, 
        related_name='jobs', 
        blank=True
    )
    topics = models.ManyToManyField(
        Topic, 
        related_name='jobs', 
        blank=True
    )
    images = models.ManyToManyField(
        'JobImage', 
        related_name='jobs', 
        blank=True
    )
    description = models.TextField()
    remarks = models.TextField()
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        db_index=True
    )
    priority = models.CharField(
        max_length=20, 
        choices=PRIORITY_CHOICES, 
        default='medium'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Maintenance Jobs'
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self):
        return f"Job {self.job_id} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if not self.job_id:
            self.job_id = self.generate_job_id()
        
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

    @classmethod
    def generate_job_id(cls):
        timestamp = timezone.now().strftime('%y')
        unique_id = get_random_string(length=6, allowed_chars='0123456789ABCDEF')
        return f"j{timestamp}{unique_id}"

class Property(models.Model):
    property_id = models.CharField(
        max_length=50, 
        unique=True, 
        blank=True, 
        editable=False
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    rooms = models.ManyToManyField(
        Room, 
        related_name='properties', 
        blank=True
    )
    users = models.ManyToManyField(
        User,
        related_name='accessible_properties'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.property_id:
            self.property_id = f"P{get_random_string(length=8, allowed_chars='0123456789ABCDEF')}"
        super().save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    positions = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    properties = models.ManyToManyField(
        Property,
        related_name='user_profiles',
        blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"