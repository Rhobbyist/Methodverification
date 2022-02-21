# Generated by Django 3.0.5 on 2020-06-03 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0051_auto_20200603_0952'),
    ]

    operations = [
        migrations.CreateModel(
            name='PTback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, verbose_name='子验证指标')),
                ('general', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='通用性参数设置')),
            ],
            options={
                'verbose_name': 'PT',
                'verbose_name_plural': 'PT',
            },
        ),
        migrations.AlterField(
            model_name='pjjmd',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='通用性参数设置'),
        ),
        migrations.AlterField(
            model_name='pjjmd',
            name='name',
            field=models.CharField(blank=True, max_length=32, verbose_name='子验证指标'),
        ),
        migrations.AlterField(
            model_name='pnjmd',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='通用性参数设置'),
        ),
        migrations.AlterField(
            model_name='pnjmd',
            name='name',
            field=models.CharField(blank=True, max_length=32, verbose_name='子验证指标'),
        ),
        migrations.CreateModel(
            name='PTbacktexts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=200, verbose_name='描述性内容')),
                ('pTback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.PTback', verbose_name='PT')),
            ],
            options={
                'verbose_name': '描述性内容',
                'verbose_name_plural': '描述性内容',
            },
        ),
        migrations.CreateModel(
            name='PTbackMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minSample', models.FloatField(verbose_name='所需最小样本数')),
                ('minPass', models.FloatField(verbose_name='最低通过率CV(%)')),
                ('pTback', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='report.PTback', verbose_name='PT')),
            ],
            options={
                'verbose_name': '基本参数',
                'verbose_name_plural': '基本参数',
            },
        ),
    ]
