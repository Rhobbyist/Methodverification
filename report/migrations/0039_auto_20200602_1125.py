# Generated by Django 3.0.5 on 2020-06-02 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0038_auto_20200602_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jmdbackstage',
            name='index',
            field=models.CharField(blank=True, max_length=32, verbose_name='子验证指标'),
        ),
    ]
