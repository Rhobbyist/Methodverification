# Generated by Django 3.0.5 on 2020-06-02 01:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0032_auto_20200602_0908'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='general',
            name='name',
        ),
        migrations.RemoveField(
            model_name='jmdbackstage',
            name='index',
        ),
        migrations.RemoveField(
            model_name='pjjmdbackstage',
            name='name',
        ),
        migrations.RemoveField(
            model_name='pnjmdbackstage',
            name='name',
        ),
    ]
