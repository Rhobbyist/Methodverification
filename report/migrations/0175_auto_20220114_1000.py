# Generated by Django 3.0.5 on 2022-01-14 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0174_stability_stabilitygeneral_stabilitygeneralmethod_stabilitygeneraltexts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stability',
            old_name='samplenametemperature',
            new_name='temperature',
        ),
    ]
