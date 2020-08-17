# Generated by Django 2.2.7 on 2020-07-15 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardCedi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod_bodega', models.IntegerField()),
                ('nom_bodega', models.CharField(max_length=100)),
                ('categoria_id', models.IntegerField()),
                ('nom_categoria', models.CharField(max_length=100)),
                ('cod_negocio', models.IntegerField()),
                ('nom_negocio', models.CharField(max_length=100)),
                ('cod_line', models.IntegerField()),
                ('nom_linea', models.CharField(max_length=100)),
                ('cod_marca', models.IntegerField()),
                ('nom_marca', models.CharField(max_length=100)),
                ('cod_articulo', models.DecimalField(decimal_places=2, max_digits=8)),
                ('estiba_devolucion', models.DecimalField(decimal_places=2, max_digits=8)),
                ('estiba_transito', models.DecimalField(decimal_places=2, max_digits=8)),
                ('estiba_no_apta', models.DecimalField(decimal_places=2, max_digits=8)),
                ('cantidad_total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('estibas', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
            options={
                'db_table': 'general_almacenamiento',
                'managed': False,
            },
        ),
    ]
