# Generated by Django 3.2.8 on 2022-02-11 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0177_prepared_sample_stability_special_prepared_sample_stability_special_method_prepared_sample_stability'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prepared_sample_stability_special_method',
            name='prepared_Sample_Stability_special',
        ),
        migrations.RemoveField(
            model_name='prepared_sample_stability_special_texts',
            name='prepared_Sample_Stability_special',
        ),
        migrations.DeleteModel(
            name='Prepared_Sample_Stability_special',
        ),
        migrations.DeleteModel(
            name='Prepared_Sample_Stability_special_method',
        ),
        migrations.DeleteModel(
            name='Prepared_Sample_Stability_special_texts',
        ),
    ]
