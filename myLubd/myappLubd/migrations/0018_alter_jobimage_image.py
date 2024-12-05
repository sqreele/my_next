# Generated by Django 4.2.16 on 2024-12-05 15:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myappLubd', '0017_remove_jobimage_file_size_remove_jobimage_height_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobimage',
            name='image',
            field=models.ImageField(blank=True, help_text='Uploaded image file', null=True, upload_to='maintenance_job_images/%Y/%m/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif', 'webp'])]),
        ),
    ]
