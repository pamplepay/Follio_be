# Generated by Django 3.1.7 on 2021-09-26 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0018_auto_20210926_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='chartdetail',
            name='insurance_type',
            field=models.SmallIntegerField(choices=[(0, '공통'), (1, '생명보험'), (2, '손해보험')], default=0),
        ),
    ]