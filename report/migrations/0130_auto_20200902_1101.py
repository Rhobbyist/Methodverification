# Generated by Django 3.0.5 on 2020-09-02 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0129_auto_20200901_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pt',
            name='PT_pass',
        ),
        migrations.RemoveField(
            model_name='pt',
            name='bias',
        ),
        migrations.RemoveField(
            model_name='pt',
            name='received',
        ),
        migrations.RemoveField(
            model_name='pt',
            name='target',
        ),
        migrations.RemoveField(
            model_name='pt',
            name='value',
        ),
        migrations.RemoveField(
            model_name='recycle',
            name='end_conc1',
        ),
        migrations.RemoveField(
            model_name='recycle',
            name='end_conc2',
        ),
        migrations.RemoveField(
            model_name='recycle',
            name='end_conc3',
        ),
        migrations.RemoveField(
            model_name='recycle',
            name='end_recycle1',
        ),
        migrations.RemoveField(
            model_name='recycle',
            name='end_recycle2',
        ),
        migrations.RemoveField(
            model_name='recycle',
            name='end_recycle3',
        ),
        migrations.RemoveField(
            model_name='recycle',
            name='sam_conc',
        ),
        migrations.RemoveField(
            model_name='recycle',
            name='theory_conc',
        ),
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
            model_name='amrgeneral',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='方法学报告性能验证指标'),
        ),
        migrations.AlterField(
            model_name='amrpicture',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='carryover',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='carryovergeneral',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='方法学报告性能验证指标'),
        ),
        migrations.AlterField(
            model_name='crr',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='crrgeneral',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='方法学报告性能验证指标'),
        ),
        migrations.AlterField(
            model_name='endconclusion',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='interprecisiongeneral',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='方法学报告性能验证指标'),
        ),
        migrations.AlterField(
            model_name='jmd',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='lod',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='matrixeffect',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='matrixeffectgeneral',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='方法学报告性能验证指标'),
        ),
        migrations.AlterField(
            model_name='ms',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='msgeneral',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='方法学报告性能验证指标'),
        ),
        migrations.AlterField(
            model_name='pt',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='ptgeneral',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='方法学报告性能验证指标'),
        ),
        migrations.AlterField(
            model_name='recycle',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='recyclegeneral',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='方法学报告性能验证指标'),
        ),
        migrations.AlterField(
            model_name='repeatprecisiongeneral',
            name='general',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='report.General', verbose_name='方法学报告性能验证指标'),
        ),
        migrations.AlterField(
            model_name='validation_reason',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='yx_method',
            name='Flowrate',
            field=models.CharField(blank=True, max_length=200, verbose_name='流速(mL/min)'),
        ),
        migrations.AlterField(
            model_name='yx_method',
            name='Mobile_phaseA',
            field=models.CharField(blank=True, max_length=200, verbose_name='流动相A'),
        ),
        migrations.AlterField(
            model_name='yx_method',
            name='Mobile_phaseB',
            field=models.CharField(blank=True, max_length=200, verbose_name='流动相B'),
        ),
        migrations.AlterField(
            model_name='yx_method',
            name='step',
            field=models.CharField(blank=True, max_length=200, verbose_name='步骤'),
        ),
        migrations.AlterField(
            model_name='yx_method',
            name='time',
            field=models.CharField(blank=True, max_length=200, verbose_name='分析时间(min)'),
        ),
        migrations.AlterField(
            model_name='yx_methodtexts',
            name='text',
            field=models.TextField(max_length=500, verbose_name='描述性内容'),
        ),
        migrations.AlterField(
            model_name='zp_method',
            name='CollisionV',
            field=models.CharField(blank=True, max_length=200, verbose_name='Collision(V)'),
        ),
        migrations.AlterField(
            model_name='zp_method',
            name='ConeV',
            field=models.CharField(blank=True, max_length=200, verbose_name='Cone(V)'),
        ),
        migrations.AlterField(
            model_name='zp_method',
            name='Times',
            field=models.CharField(blank=True, max_length=200, verbose_name='Time(s)'),
        ),
        migrations.AlterField(
            model_name='zp_method',
            name='norm',
            field=models.CharField(blank=True, max_length=200, verbose_name='分析物名称'),
        ),
        migrations.AlterField(
            model_name='zp_method',
            name='precursor_ion',
            field=models.CharField(blank=True, max_length=200, verbose_name='母离子'),
        ),
        migrations.AlterField(
            model_name='zp_method',
            name='product_ion',
            field=models.CharField(blank=True, max_length=200, verbose_name='子离子'),
        ),
        migrations.AlterField(
            model_name='zp_methodtexts',
            name='text',
            field=models.TextField(max_length=500, verbose_name='描述性内容'),
        ),
    ]