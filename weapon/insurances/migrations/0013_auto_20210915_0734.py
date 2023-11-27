# Generated by Django 3.1.7 on 2021-09-14 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0012_auto_20210915_0734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerinsurance',
            name='refund_type',
            field=models.SmallIntegerField(choices=[(1, '종신보험'), (2, '만기환급'), (3, '50%환급'), (4, '순수보장형')], default=1, verbose_name='환급타입'),
        ),
    ]