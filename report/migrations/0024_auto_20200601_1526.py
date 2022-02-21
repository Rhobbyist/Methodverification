# Generated by Django 3.0.5 on 2020-06-01 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0023_general_index'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='general',
            name='index',
        ),
        migrations.AlterField(
            model_name='jmdbackstage',
            name='general',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.general', verbose_name='通用性参数设置'),
        ),
    ]