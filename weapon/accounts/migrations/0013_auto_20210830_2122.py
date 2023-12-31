# Generated by Django 3.1.7 on 2021-08-30 12:22

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_profile_recommend_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, default='', upload_to='uploads/profile/%Y/%m/%d/'),
        ),
    ]
