# Generated by Django 2.2.7 on 2020-09-11 03:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import etl.models


class Migration(migrations.Migration):

    dependencies = [
        ('etl', '0002_auto_20200630_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errorlog',
            name='code',
            field=models.IntegerField(verbose_name='Código de error'),
        ),
        migrations.AlterField(
            model_name='errorlog',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Descripción del Error'),
        ),
        migrations.AlterField(
            model_name='errorlog',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='etl.ErrorType', verbose_name='Tipo de Error'),
        ),
        migrations.AlterField(
            model_name='errortype',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Tipo de Error'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='account.Company', verbose_name='Empresa'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Carga'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='file',
            field=models.FileField(upload_to=etl.models.user_directory_path, validators=[django.core.validators.FileExtensionValidator(['csv'])], verbose_name='Archivo .csv'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='max',
            field=models.IntegerField(default=10000, verbose_name='Camtidad Máxima de Registros'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='min',
            field=models.IntegerField(default=1, verbose_name='Cantidad mínima de registros'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Nombre de Carga'),
        ),
        migrations.AlterField(
            model_name='upload',
            name='separator',
            field=models.CharField(default=';', max_length=1, verbose_name='Separador de datos'),
        ),
    ]
