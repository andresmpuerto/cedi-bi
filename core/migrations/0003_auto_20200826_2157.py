# Generated by Django 2.2.7 on 2020-08-27 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_lotedim_lotedimttemp'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LoteDim',
            new_name='LotesDim',
        ),
        migrations.RenameModel(
            old_name='LoteDimTtemp',
            new_name='LotesDimTtemp',
        ),
    ]
