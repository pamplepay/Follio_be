# Generated by Django 3.1.7 on 2021-05-14 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210513_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='phonenumberuserprofile',
            name='is_editor',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='phonenumberuserprofile',
            name='is_super',
            field=models.BooleanField(default=False),
        ),
    ]
