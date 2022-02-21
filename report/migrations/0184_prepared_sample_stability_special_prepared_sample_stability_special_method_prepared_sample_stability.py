# Generated by Django 3.2.8 on 2022-02-14 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0183_auto_20220214_0648'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prepared_Sample_Stability_special',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='样品处理后稳定性', editable=False, max_length=32, verbose_name='验证指标')),
                ('special', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.special', verbose_name='特殊参数设置')),
            ],
            options={
                'verbose_name': '样品处理后稳定性',
                'verbose_name_plural': '样品处理后稳定性',
            },
        ),
        migrations.CreateModel(
            name='Prepared_Sample_Stability_special_texts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500, verbose_name='描述性内容')),
                ('prepared_Sample_Stability_special', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.prepared_sample_stability_special', verbose_name='样品处理后稳定性')),
            ],
            options={
                'verbose_name': '描述性内容',
                'verbose_name_plural': '描述性内容',
            },
        ),
        migrations.CreateModel(
            name='Prepared_Sample_Stability_special_method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lowvalue', models.FloatField(blank=True, verbose_name='回收率下限(%)')),
                ('upvalue', models.FloatField(blank=True, verbose_name='回收率上限(%)')),
                ('prepared_Sample_Stability_special', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='report.prepared_sample_stability_special', verbose_name='样品处理后稳定性')),
            ],
            options={
                'verbose_name': '基本参数',
                'verbose_name_plural': '基本参数',
            },
        ),
    ]