# Generated by Django 4.2.16 on 2024-12-05 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myappLubd', '0011_remove_jobimage_file_size_remove_jobimage_height_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobimage',
            name='description',
        ),
    ]
