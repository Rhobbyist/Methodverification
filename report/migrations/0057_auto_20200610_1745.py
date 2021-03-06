# Generated by Django 3.0.5 on 2020-06-10 09:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0056_auto_20200610_1743'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recycle',
            old_name='end_conc',
            new_name='end_conc1',
        ),
        migrations.RenameField(
            model_name='recycle',
            old_name='end_recycle',
            new_name='end_conc2',
        ),
        migrations.AddField(
            model_name='recycle',
            name='end_conc3',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recycle',
            name='end_recycle1',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recycle',
            name='end_recycle2',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recycle',
            name='end_recycle3',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='amrback',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='方法学报告性能验证指标'),
        ),
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
            model_name='pnjmd',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='方法学报告性能验证指标'),
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
    ]
