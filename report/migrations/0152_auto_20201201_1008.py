# Generated by Django 3.0.5 on 2020-12-01 02:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0151_auto_20201125_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amr',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='amrconsluion',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='amrgeneralmethod',
            name='cv',
            field=models.FloatField(verbose_name='最大允许CV(%)'),
        ),
        migrations.AlterField(
            model_name='amrgeneralmethod',
            name='lowvalue',
            field=models.FloatField(verbose_name='回收率下限(%)'),
        ),
        migrations.AlterField(
            model_name='amrgeneralmethod',
            name='upvalue',
            field=models.FloatField(verbose_name='回收率上限(%)'),
        ),
        migrations.AlterField(
            model_name='amrpicture',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='amrspecialmethod',
            name='cv',
            field=models.FloatField(verbose_name='最大允许CV(%)'),
        ),
        migrations.AlterField(
            model_name='amrspecialmethod',
            name='lowvalue',
            field=models.FloatField(verbose_name='回收率下限(%)'),
        ),
        migrations.AlterField(
            model_name='amrspecialmethod',
            name='upvalue',
            field=models.FloatField(verbose_name='回收率上限(%)'),
        ),
        migrations.AlterField(
            model_name='carryover',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='carryover2',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='carryovergeneralmethod',
            name='acceptable',
            field=models.FloatField(verbose_name='可接受标准(%)'),
        ),
        migrations.AlterField(
            model_name='carryoverspecialmethod',
            name='accept',
            field=models.FloatField(verbose_name='可接受标准(%)'),
        ),
        migrations.AlterField(
            model_name='crr',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='crr2',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='crrgeneralmethod',
            name='lowvalue',
            field=models.FloatField(verbose_name='回收率下限(%)'),
        ),
        migrations.AlterField(
            model_name='crrgeneralmethod',
            name='upvalue',
            field=models.FloatField(verbose_name='回收率上限(%)'),
        ),
        migrations.AlterField(
            model_name='crrspecialmethod',
            name='lowvalue',
            field=models.FloatField(verbose_name='回收率下限(%)'),
        ),
        migrations.AlterField(
            model_name='crrspecialmethod',
            name='upvalue',
            field=models.FloatField(verbose_name='回收率上限(%)'),
        ),
        migrations.AlterField(
            model_name='endconclusion',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='interprecisiongeneralmethod',
            name='minSample',
            field=models.IntegerField(verbose_name='所需最小样本数'),
        ),
        migrations.AlterField(
            model_name='interprecisionspecialmethod',
            name='minSample',
            field=models.IntegerField(verbose_name='所需最小样本数'),
        ),
        migrations.AlterField(
            model_name='jmd',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='matrixeffect',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='matrixeffectgeneralmethod',
            name='bias',
            field=models.FloatField(verbose_name='最大允许偏差'),
        ),
        migrations.AlterField(
            model_name='matrixeffectspecialmethod',
            name='bias',
            field=models.FloatField(verbose_name='最大允许偏差'),
        ),
        migrations.AlterField(
            model_name='ms',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='pt',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='ptgeneralmethod',
            name='minSample',
            field=models.IntegerField(blank=True, verbose_name='所需最小样本数'),
        ),
        migrations.AlterField(
            model_name='ptspecialmethod',
            name='minSample',
            field=models.IntegerField(verbose_name='所需最小样本数'),
        ),
        migrations.AlterField(
            model_name='recycle',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='recyclegeneralmethod',
            name='lowvalue',
            field=models.FloatField(verbose_name='回收率下限(%)'),
        ),
        migrations.AlterField(
            model_name='recyclegeneralmethod',
            name='upvalue',
            field=models.FloatField(verbose_name='回收率上限(%)'),
        ),
        migrations.AlterField(
            model_name='recyclespecialmethod',
            name='lowvalue',
            field=models.FloatField(verbose_name='回收率下限(%)'),
        ),
        migrations.AlterField(
            model_name='recyclespecialmethod',
            name='upvalue',
            field=models.FloatField(verbose_name='回收率上限(%)'),
        ),
        migrations.AlterField(
            model_name='repeatprecisiongeneralmethod',
            name='maxCV',
            field=models.FloatField(verbose_name='最大允许CV(%)'),
        ),
        migrations.AlterField(
            model_name='repeatprecisiongeneralmethod',
            name='minSample',
            field=models.IntegerField(verbose_name='所需最小样本数'),
        ),
        migrations.AlterField(
            model_name='repeatprecisionspecialmethod',
            name='minSample',
            field=models.IntegerField(verbose_name='所需最小样本数'),
        ),
        migrations.AlterField(
            model_name='validation_reason',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.DeleteModel(
            name='LOD',
        ),
    ]