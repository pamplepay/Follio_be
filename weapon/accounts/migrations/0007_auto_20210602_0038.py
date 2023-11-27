# Generated by Django 3.1.7 on 2021-06-01 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_delete_betauser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='is_agree_marketing',
            new_name='is_first_visit',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_editor',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_super',
        ),
        migrations.AddField(
            model_name='profile',
            name='kakao_thumbnail',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]