# Generated by Django 3.0.5 on 2020-06-02 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0042_auto_20200602_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='method',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.Item', verbose_name='项目名称'),
        ),
    ]
