# Generated by Django 3.2.8 on 2022-02-11 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0178_auto_20220211_0654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stabilityspecial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, editable=False, max_length=32, verbose_name='验证指标')),
                ('special', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.special', verbose_name='方法学报告性能验证指标')),
            ],
            options={
                'verbose_name': '样品稳定性',
                'verbose_name_plural': '样品稳定性',
            },
        ),
        migrations.CreateModel(
            name='Stabilityspecialtexts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500, verbose_name='描述性内容')),
                ('stabilityspecial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.stabilityspecial', verbose_name='')),
            ],
            options={
                'verbose_name': '描述性内容',
                'verbose_name_plural': '描述性内容',
            },
        ),
        migrations.CreateModel(
            name='Stabilityspecialmethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lowvalue', models.FloatField(verbose_name='回收率下限(%)')),
                ('upvalue', models.FloatField(verbose_name='回收率上限(%)')),
                ('stabilityspecial', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='report.stabilityspecial', verbose_name='回收率')),
            ],
            options={
                'verbose_name': '基本参数',
                'verbose_name_plural': '基本参数',
            },
        ),
    ]