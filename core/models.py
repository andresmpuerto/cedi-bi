from django.core.validators import FileExtensionValidator
from django.db import models

from account.models import Company


def user_directory_path(instance, filename):
    return 'csv/template/company_{0}/{1}'.format(instance.company.id, filename)


class CategoriasBodegasDim(models.Model):
    nom_categoria = models.CharField(max_length=100, verbose_name='Nombre de Categoría')

    class Meta:
        verbose_name = 'Categorías de Bodega'


class UploadTemplaCSV(models.Model):
    file = models.FileField(upload_to=user_directory_path,
                            validators=[FileExtensionValidator(['csv'])],
                            verbose_name="Archivo Plantilla .csv"
                            )
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, verbose_name='Compañía')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False, verbose_name="Fecha de Carga")
    updated_at = models.DateTimeField(auto_now=True, blank=True, editable=False)

    class Meta:
        verbose_name = 'Cargar Plantilla CSV'


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
    cod_marca = models.CharField(max_length=10)
    nom_marca = models.CharField(max_length=100)
    cod_linea = models.IntegerField()


class ArticulosDimTtemp(models.Model):
    cod_articulo = models.IntegerField()
    nom_articulo = models.CharField(max_length=100)
    presentacion = models.CharField(max_length=12)
    unidad_venta = models.IntegerField()
    factor_estiba = models.DecimalField(decimal_places=2, max_digits=8)
    inventario_seguridad = models.IntegerField(null=True)
    cod_marca = models.CharField(max_length=10)


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
    cod_marca = models.CharField(max_length=10)
    nom_marca = models.CharField(max_length=100)
    cod_linea = models.IntegerField()


class ArticulosDim(models.Model):
    cod_articulo = models.IntegerField()
    nom_articulo = models.CharField(max_length=100)
    presentacion = models.CharField(max_length=12)
    unidad_venta = models.IntegerField()
    factor_estiba = models.DecimalField(decimal_places=2, null=True, max_digits=8)
    inventario_seguridad = models.IntegerField(null=True)
    cod_marca = models.CharField(max_length=10)


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
    cod_bodega = models.CharField(max_length=10)
    cod_negocio = models.IntegerField()
    cod_linea = models.IntegerField()
    cod_marca = models.CharField(max_length=10)
    cod_articulo = models.IntegerField()
