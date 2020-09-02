from django.db import models


class CategoriasBodegasDim(models.Model):
    nom_categoria = models.CharField(max_length=100)


class BodegasDimTtemp(models.Model):
    cod_bodega = models.CharField(max_length=10)
    nom_bodega = models.CharField(max_length=100)
    categoria = models.ForeignKey(CategoriasBodegasDim, on_delete=models.DO_NOTHING, null=True)


class LotesDimTtemp(models.Model):
    cod_lote = models.CharField(max_length=10)
    cod_articulo = models.CharField(max_length=10)
    fecha_fab = models.IntegerField()
    fecha_vencimiento = models.IntegerField()


class NegociosDimTtemp(models.Model):
    cod_negocio = models.IntegerField()
    nom_negocio = models.CharField(max_length=100)


class LineasDimTtemp(models.Model):
    cod_linea = models.IntegerField()
    nom_linea = models.CharField(max_length=100)
    cod_negocio = models.IntegerField()


class MarcasDimTtemp(models.Model):
    cod_marca = models.IntegerField()
    nom_marca = models.CharField(max_length=100)
    cod_linea = models.IntegerField()


class ArticulosDimTtemp(models.Model):
    cod_articulo = models.IntegerField()
    nom_articulo = models.CharField(max_length=100)
    presentacion = models.CharField(max_length=12)
    unidad_venta = models.IntegerField()
    factor_estiba = models.DecimalField(decimal_places=2, max_digits=8)
    inventario_seguridad = models.IntegerField(null=True)
    cod_marca = models.IntegerField()


# ###################
class BodegasDim(models.Model):
    cod_bodega = models.CharField(max_length=10)
    nom_bodega = models.CharField(max_length=100)
    categoria = models.ForeignKey(CategoriasBodegasDim, on_delete=models.DO_NOTHING)


class LotesDim(models.Model):
    cod_lote = models.CharField(max_length=10)
    cod_articulo = models.CharField(max_length=10)
    fecha_fab = models.IntegerField()
    fecha_vencimiento = models.IntegerField()


class NegociosDim(models.Model):
    cod_negocio = models.IntegerField()
    nom_negocio = models.CharField(max_length=100)


class LineasDim(models.Model):
    cod_linea = models.IntegerField()
    nom_linea = models.CharField(max_length=100)
    cod_negocio = models.IntegerField()


class MarcasDim(models.Model):
    cod_marca = models.IntegerField()
    nom_marca = models.CharField(max_length=100)
    cod_linea = models.IntegerField()


class ArticulosDim(models.Model):
    cod_articulo = models.IntegerField()
    nom_articulo = models.CharField(max_length=100)
    presentacion = models.CharField(max_length=12)
    unidad_venta = models.IntegerField()
    factor_estiba = models.DecimalField(decimal_places=2, null=True, max_digits=8)
    inventario_seguridad = models.IntegerField(null=True)
    cod_marca = models.IntegerField()


class FactAlmacenamiento(models.Model):
    cantidad_inicial = models.DecimalField(decimal_places=2, max_digits=8)
    cantidad_entradas = models.DecimalField(decimal_places=2, max_digits=8)
    cantidad_salidas = models.DecimalField(decimal_places=2, max_digits=8)
    cantidad_ventas = models.DecimalField(decimal_places=2, max_digits=8)
    cantidad_devolucion = models.DecimalField(decimal_places=2, max_digits=8)
    cantidad_existencias = models.DecimalField(decimal_places=2, max_digits=8)
    cantidad_separacion = models.DecimalField(decimal_places=2, max_digits=8)
    cantidad_reserva = models.DecimalField(decimal_places=2, max_digits=8)
    cantidad_transito = models.DecimalField(decimal_places=2, max_digits=8)
    cantidad_no_apta = models.DecimalField(decimal_places=2, max_digits=8)
    fecha_registro = models.CharField(max_length=8)
    cod_bodega = models.IntegerField()
    cod_negocio = models.IntegerField()
    cod_linea = models.IntegerField()
    cod_marca = models.IntegerField()
    cod_articulo = models.IntegerField()
