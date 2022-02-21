# Generated by Django 3.0.5 on 2020-06-03 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0048_auto_20200603_0925'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pnjmdmethod',
            options={'verbose_name': '基本参数', 'verbose_name_plural': '基本参数'},
        ),
        migrations.AlterModelOptions(
            name='pnjmdtexts',
            options={'verbose_name': '描述性内容', 'verbose_name_plural': '描述性内容'},
        ),
        migrations.AddField(
            model_name='general',
            name='name',
            field=models.CharField(default='', max_length=32, verbose_name='通用性参数设置'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pnjmd',
            name='general',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='通用性参数设置'),
        ),
    ]
