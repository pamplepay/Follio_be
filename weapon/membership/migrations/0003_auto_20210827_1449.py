# Generated by Django 3.1.7 on 2021-08-27 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0002_auto_20210827_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='product_amount',
            field=models.IntegerField(default=0, verbose_name='멤버십 가격'),
        ),
    ]