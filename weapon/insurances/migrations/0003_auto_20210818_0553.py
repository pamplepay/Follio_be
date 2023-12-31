# Generated by Django 3.1.7 on 2021-08-17 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0002_auto_20210818_0522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerinsurancedetail',
            name='assurance_amount',
            field=models.SmallIntegerField(blank=True, default=None, null=True, verbose_name='보장 금액'),
        ),
        migrations.AlterField(
            model_name='customerinsurancedetail',
            name='payment_period',
            field=models.SmallIntegerField(blank=True, default=None, null=True, verbose_name='납입기간'),
        ),
        migrations.AlterField(
            model_name='customerinsurancedetail',
            name='premium',
            field=models.SmallIntegerField(blank=True, default=None, null=True, verbose_name='보험료'),
        ),
        migrations.AlterField(
            model_name='customerinsurancedetail',
            name='warranty_period',
            field=models.CharField(blank=True, default=None, max_length=20, null=True, verbose_name='보증기간'),
        ),
    ]
