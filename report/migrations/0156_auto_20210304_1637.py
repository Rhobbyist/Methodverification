# Generated by Django 3.0.5 on 2021-03-04 08:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0155_auto_20201215_0945'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jcxgeneral',
            options={'verbose_name': '检出限', 'verbose_name_plural': '检出限'},
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
            model_name='amrpicture',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='amrspecial',
            name='name',
            field=models.CharField(blank=True, default='线性灵敏度和线性范围', editable=False, max_length=32, verbose_name='验证指标'),
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
            model_name='carryoverspecial',
            name='name',
            field=models.CharField(blank=True, default='携带效应', editable=False, max_length=32, verbose_name='验证指标'),
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
            model_name='crrspecial',
            name='name',
            field=models.CharField(blank=True, default='临床可报告范围', editable=False, max_length=32, verbose_name='验证指标'),
        ),
        migrations.AlterField(
            model_name='endconclusion',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='interprecisionspecial',
            name='name',
            field=models.CharField(blank=True, default='中间精密度', editable=False, max_length=32, verbose_name='验证指标'),
        ),
        migrations.AlterField(
            model_name='jcxspecial',
            name='name',
            field=models.CharField(blank=True, default='检出限', editable=False, max_length=32, verbose_name='验证指标'),
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
            model_name='lodpicture',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='matrixeffect',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='matrixeffectspecial',
            name='name',
            field=models.CharField(blank=True, default='基质效应', editable=False, max_length=32, verbose_name='验证指标'),
        ),
        migrations.AlterField(
            model_name='ms',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='msspecial',
            name='name',
            field=models.CharField(blank=True, default='基质特异性', editable=False, max_length=32, verbose_name='验证指标'),
        ),
        migrations.AlterField(
            model_name='pt',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='ptspecial',
            name='name',
            field=models.CharField(blank=True, default='PT', editable=False, max_length=32, verbose_name='验证指标'),
        ),
        migrations.AlterField(
            model_name='recycle',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='recyclespecial',
            name='name',
            field=models.CharField(blank=True, default='加标回收率', editable=False, max_length=32, verbose_name='验证指标'),
        ),
        migrations.AlterField(
            model_name='repeatprecisionspecial',
            name='name',
            field=models.CharField(blank=True, default='重复性精密度', editable=False, max_length=32, verbose_name='验证指标'),
        ),
        migrations.AlterField(
            model_name='special',
            name='Effective_digits',
            field=models.IntegerField(verbose_name='有效位数'),
        ),
        migrations.AlterField(
            model_name='special',
            name='Number_of_compounds',
            field=models.IntegerField(verbose_name='化合物个数'),
        ),
        migrations.AlterField(
            model_name='validation_reason',
            name='reportinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.ReportInfo'),
        ),
        migrations.AlterField(
            model_name='zp_method',
            name='norm',
            field=models.CharField(max_length=200, verbose_name='分析物名称'),
        ),
        migrations.AlterField(
            model_name='zp_method',
            name='precursor_ion',
            field=models.CharField(max_length=200, verbose_name='母离子(m/z)'),
        ),
        migrations.AlterField(
            model_name='zp_method',
            name='product_ion',
            field=models.CharField(max_length=200, verbose_name='子离子(m/z)'),
        ),
    ]