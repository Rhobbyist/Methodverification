# Generated by Django 3.0.5 on 2020-06-01 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0021_auto_20200601_1449'),
    ]

    operations = [
        migrations.CreateModel(
            name='baseparameterjmd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baseparameter', models.CharField(max_length=32, verbose_name='基本参数')),
            ],
            options={
                'verbose_name': '基本参数',
                'verbose_name_plural': '基本参数',
            },
        ),
        migrations.CreateModel(
            name='jmdbackstage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.CharField(max_length=32, verbose_name='子验证指标')),
            ],
            options={
                'verbose_name': '精密度',
                'verbose_name_plural': '精密度',
            },
        ),
        migrations.CreateModel(
            name='textjmd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=200, verbose_name='描述性内容')),
                ('jmdbackstage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.jmdbackstage')),
            ],
            options={
                'verbose_name': '描述性内容',
                'verbose_name_plural': '描述性内容',
            },
        ),
        migrations.RemoveField(
            model_name='subindex',
            name='general',
        ),
        migrations.RemoveField(
            model_name='general',
            name='index',
        ),
        migrations.DeleteModel(
            name='parametersetting',
        ),
        migrations.DeleteModel(
            name='subindex',
        ),
        migrations.AddField(
            model_name='jmdbackstage',
            name='general',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='report.general', verbose_name='通用性参数设置'),
        ),
        migrations.AddField(
            model_name='baseparameterjmd',
            name='jmdbackstage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.jmdbackstage'),
        ),
    ]
