# Generated by Django 3.0.5 on 2020-05-27 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0015_remove_ptbackstage_ptnormtarget'),
    ]

    operations = [
        migrations.AddField(
            model_name='ptbackstage',
            name='PTnormtarget',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
