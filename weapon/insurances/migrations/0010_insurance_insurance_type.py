# Generated by Django 3.1.7 on 2021-09-08 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0009_insurancetemplate_is_common'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurance',
            name='insurance_type',
            field=models.SmallIntegerField(choices=[(1, '생명보험'), (2, '손해보험')], default=1),
        ),
    ]
