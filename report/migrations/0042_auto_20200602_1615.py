# Generated by Django 3.0.5 on 2020-06-02 08:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0041_auto_20200602_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='general',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='通用性参数设置')),
            ],
            options={
                'verbose_name': '通用性参数设置',
                'verbose_name_plural': '通用性参数设置',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('subitem', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='子验证指标')),
                ('general', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.general', verbose_name='添加新验证指标')),
            ],
            options={
                'verbose_name': '子验证指标',
                'verbose_name_plural': '子验证指标',
            },
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minSample', models.FloatField(verbose_name='所需最小样本数')),
                ('maxCV', models.FloatField(verbose_name='最大允许CV(%)')),
                ('text', models.TextField(max_length=200, verbose_name='描述性内容')),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='report.Item', verbose_name='项目名称')),
            ],
            options={
                'verbose_name': '基本参数',
                'verbose_name_plural': '基本参数',
            },
        ),
        migrations.RemoveField(
            model_name='modeltwo',
            name='relation_model_one',
        ),
        migrations.DeleteModel(
            name='ModelOne',
        ),
        migrations.DeleteModel(
            name='ModelTwo',
        ),
    ]
