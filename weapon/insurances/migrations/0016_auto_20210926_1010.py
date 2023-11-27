# Generated by Django 3.1.7 on 2021-09-26 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('insurances', '0015_auto_20210925_0632'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insurance_type', models.SmallIntegerField(choices=[(0, '공통'), (1, '생명보험'), (2, '손해보험')], default=0)),
                ('name', models.CharField(max_length=20)),
                ('order', models.SmallIntegerField(blank=True, default=0, verbose_name='순서')),
            ],
            options={
                'verbose_name': '분석 카테고리',
                'verbose_name_plural': '분석 카테고리',
            },
        ),
        migrations.CreateModel(
            name='AnalysisDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chart_type', models.SmallIntegerField(choices=[(1, 'Cart1'), (2, 'Cart2')], default=1)),
                ('name', models.CharField(max_length=20)),
                ('order', models.SmallIntegerField(blank=True, default=0, verbose_name='순서')),
                ('chart_based_amount', models.SmallIntegerField(blank=True, default=0, verbose_name='차트 기준 금액')),
            ],
            options={
                'verbose_name': '분석 상세 아이템',
                'verbose_name_plural': '분석 상세 아이템',
            },
        ),
        migrations.CreateModel(
            name='AnalysisSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insurance_type', models.SmallIntegerField(choices=[(0, '공통'), (1, '생명보험'), (2, '손해보험')], default=0)),
                ('name', models.CharField(max_length=20)),
                ('order', models.SmallIntegerField(blank=True, default=0, verbose_name='순서')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='insurances.analysiscategory')),
            ],
            options={
                'verbose_name': '분석 서브 카테고리',
                'verbose_name_plural': '분석 서브 카테고리',
            },
        ),
        migrations.RemoveField(
            model_name='insurancetemplatedetail',
            name='detail',
        ),
        migrations.RemoveField(
            model_name='insurancetemplatedetail',
            name='insurance',
        ),
        migrations.AlterField(
            model_name='insurancedetail',
            name='chart_type',
            field=models.SmallIntegerField(choices=[(1, 'Cart1'), (2, 'Cart2')], default=1),
        ),
        migrations.DeleteModel(
            name='InsuranceTemplate',
        ),
        migrations.DeleteModel(
            name='InsuranceTemplateDetail',
        ),
        migrations.AddField(
            model_name='analysisdetail',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='insurances.analysissubcategory'),
        ),
    ]
