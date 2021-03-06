# Generated by Django 3.0.5 on 2020-06-01 02:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0019_auto_20200601_1031'),
    ]

    operations = [
        migrations.CreateModel(
            name='parametersetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('baseparameter', models.CharField(max_length=32, verbose_name='基本参数')),
                ('text', models.CharField(max_length=200, verbose_name='描述性内容')),
                ('subindex', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.subindex')),
            ],
            options={
                'verbose_name': '参数设置',
                'verbose_name_plural': '参数设置',
            },
        ),
    ]
