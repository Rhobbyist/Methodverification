# Generated by Django 3.0.5 on 2020-06-03 01:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0046_auto_20200603_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='pnjmd',
            name='name',
            field=models.CharField(default='', max_length=32, verbose_name='批内精密度'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pnjmd',
            name='general',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='通用性参数设置'),
        ),
    ]
