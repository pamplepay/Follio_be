# Generated by Django 3.1.7 on 2021-08-18 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0003_auto_20210818_0553'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurancedetail',
            name='chart_based_amount',
            field=models.SmallIntegerField(blank=True, default=0, verbose_name='차트 기준 금액'),
        ),
    ]
