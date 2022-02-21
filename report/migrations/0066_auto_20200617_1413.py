# Generated by Django 3.0.5 on 2020-06-17 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0065_auto_20200616_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jmd',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='pjjmd',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='方法学报告性能验证指标'),
        ),
        migrations.AlterField(
            model_name='pjjmdmethod',
            name='PJJMD_key',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='report.PJJMD', verbose_name='中间精密度'),
        ),
        migrations.AlterField(
            model_name='pjjmdtexts',
            name='PJJMD_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.PJJMD', verbose_name='中间精密度'),
        ),
        migrations.AlterField(
            model_name='pjjmdtexts',
            name='text',
            field=models.TextField(blank=True, max_length=200, verbose_name='描述性内容'),
        ),
        migrations.AlterField(
            model_name='pnjmd',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='方法学报告性能验证指标'),
        ),
        migrations.AlterField(
            model_name='pnjmdmethod',
            name='PNJMD_key',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='report.PNJMD', verbose_name='重复性精密度'),
        ),
        migrations.AlterField(
            model_name='pnjmdtexts',
            name='PNJMD_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.PNJMD', verbose_name='重复性精密度'),
        ),
        migrations.AlterField(
            model_name='pnjmdtexts',
            name='text',
            field=models.TextField(blank=True, max_length=200, verbose_name='描述性内容'),
        ),
        migrations.AlterField(
            model_name='pt',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='ptback',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='方法学报告性能验证指标'),
        ),
        migrations.AlterField(
            model_name='recycle',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='recycleback',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='方法学报告性能验证指标'),
        ),
        migrations.AlterField(
            model_name='recyclebackmethod',
            name='RECYCLEback_key',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='report.RECYCLEback', verbose_name='加标回收率'),
        ),
        migrations.AlterField(
            model_name='recyclebacktexts',
            name='RECYCLEback_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.RECYCLEback', verbose_name='加标回收率'),
        ),
    ]
