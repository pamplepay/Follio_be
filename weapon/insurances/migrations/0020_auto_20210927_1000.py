# Generated by Django 3.1.7 on 2021-09-27 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0019_chartdetail_insurance_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customerinsurance',
            options={'verbose_name': '포트폴리오', 'verbose_name_plural': '포트폴리오'},
        ),
        migrations.AlterField(
            model_name='customerinsurance',
            name='payment_period',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='납입기간'),
        ),
        migrations.AlterField(
            model_name='customerinsurance',
            name='percent_cancellation_refund',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='혜약 환급금 퍼센트'),
        ),
        migrations.AlterField(
            model_name='customerinsurance',
            name='portfolio_type',
            field=models.SmallIntegerField(choices=[(0, '템플릿'), (1, '기존'), (2, '제안')], default=0, verbose_name='포트폴리오 타입'),
        ),
        migrations.AlterField(
            model_name='customerinsurance',
            name='renewal_growth_rate',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='갱신 증가율'),
        ),
        migrations.AlterField(
            model_name='customerinsurance',
            name='warranty_period',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='보장기간'),
        ),
        migrations.AlterField(
            model_name='customerinsurancedetail',
            name='assurance_amount',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='보장 금액'),
        ),
        migrations.AlterField(
            model_name='customerinsurancedetail',
            name='payment_period',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='납입기간'),
        ),
        migrations.AlterField(
            model_name='customerinsurancedetail',
            name='premium',
            field=models.IntegerField(blank=True, default=None, null=True, verbose_name='보험료'),
        ),
    ]