# Generated by Django 3.0.5 on 2020-06-02 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0035_auto_20200602_0933'),
    ]

    operations = [
        migrations.CreateModel(
            name='PJjmdbackstage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='批间精密度')),
            ],
            options={
                'verbose_name': '批间精密度',
                'verbose_name_plural': '批间精密度',
            },
        ),
        migrations.CreateModel(
            name='PNjmdbackstage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='批内精密度')),
            ],
            options={
                'verbose_name': '批内精密度',
                'verbose_name_plural': '批内精密度',
            },
        ),
        migrations.RemoveField(
            model_name='jmdbackstage',
            name='baseparameter',
        ),
        migrations.RemoveField(
            model_name='jmdbackstage',
            name='text',
        ),
        migrations.AddField(
            model_name='general',
            name='name',
            field=models.CharField(default='', max_length=32, verbose_name='通用性参数设置'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jmdbackstage',
            name='index',
            field=models.CharField(default='', max_length=32, verbose_name='子验证指标'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='textPNjmd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=200, verbose_name='描述性内容')),
                ('PNjmdbackstage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.PNjmdbackstage')),
            ],
            options={
                'verbose_name': '描述性内容',
                'verbose_name_plural': '描述性内容',
            },
        ),
        migrations.CreateModel(
            name='textPJjmd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=200, verbose_name='描述性内容')),
                ('PJjmdbackstage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.PJjmdbackstage')),
            ],
            options={
                'verbose_name': '描述性内容',
                'verbose_name_plural': '描述性内容',
            },
        ),
        migrations.AddField(
            model_name='pnjmdbackstage',
            name='jmdbackstage',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='report.jmdbackstage', verbose_name='通用性参数设置'),
        ),
        migrations.AddField(
            model_name='pjjmdbackstage',
            name='jmdbackstage',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='report.jmdbackstage', verbose_name='通用性参数设置'),
        ),
        migrations.CreateModel(
            name='baseparameterPNjmd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baseparameter', models.CharField(max_length=32, verbose_name='基本参数')),
                ('PNjmdbackstage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.PNjmdbackstage')),
            ],
            options={
                'verbose_name': '基本参数',
                'verbose_name_plural': '基本参数',
            },
        ),
        migrations.CreateModel(
            name='baseparameterPJjmd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baseparameter', models.CharField(max_length=32, verbose_name='基本参数')),
                ('PJjmdbackstage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.PJjmdbackstage')),
            ],
            options={
                'verbose_name': '基本参数',
                'verbose_name_plural': '基本参数',
            },
        ),
    ]
