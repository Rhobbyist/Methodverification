# Generated by Django 3.0.5 on 2020-05-19 00:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0008_auto_20200512_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='PT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Experimentnum', models.CharField(max_length=32)),
                ('norm', models.CharField(max_length=32)),
                ('value', models.FloatField()),
                ('target', models.FloatField()),
                ('received', models.CharField(max_length=32)),
                ('bias', models.CharField(max_length=32)),
                ('reportinfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.reportInfo')),
            ],
        ),
    ]
