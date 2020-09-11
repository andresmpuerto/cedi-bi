from django.db import models
from account.models import Rol


class TypeBoard(models.Model):
    name = models.CharField(max_length=20, verbose_name="Tipo tablero")
    code = models.IntegerField(verbose_name="Código de tipo tablero")

    class Meta:
        verbose_name = "Tipos de Tablero"

    def __str__(self):
        return self.name


class Board(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre Tablero")
    description = models.CharField(max_length=120, verbose_name="Descripción Tablero")
    type = models.ForeignKey(TypeBoard, on_delete=models.DO_NOTHING, verbose_name="Tipo de Tablero")
    status = models.BooleanField(default=True, verbose_name="Activo")
    rol = models.ManyToManyField(Rol, related_name='boards', verbose_name="Roles permitidos")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, blank=True, editable=False)

    class Meta:
        verbose_name = "Tablero"

    def __str__(self):
        return self.name


class Comment(models.Model):
    message = models.CharField(max_length=140)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True, editable=False)

    class Meta:
        verbose_name = "Comentario"


class DashboardCedi(models.Model):
    cod_bodega = models.IntegerField()
    nom_bodega = models.CharField(max_length=100)
    categoria_id = models.IntegerField()
    nom_categoria = models.CharField(max_length=100)
    cod_negocio = models.IntegerField()
    nom_negocio = models.CharField(max_length=100)
    cod_linea = models.IntegerField()
    nom_linea = models.CharField(max_length=100)
    cod_marca = models.CharField(max_length=10)
    nom_marca = models.CharField(max_length=100)
    cod_articulo = models.DecimalField(max_digits=8, decimal_places=2)
    nom_articulo = models.CharField(max_length=100)
    dias_vencimiento = models.IntegerField()
    estiba_devolucion = models.DecimalField(max_digits=8, decimal_places=2)
    estiba_transito = models.DecimalField(max_digits=8, decimal_places=2)
    estiba_no_apta = models.DecimalField(max_digits=8, decimal_places=2)
    cantidad_total = models.DecimalField(max_digits=8, decimal_places=2)
    estibas = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'general_almacenamiento'


class DashboardBusiness(models.Model):
    cod_bodega = models.IntegerField()
    nom_bodega = models.CharField(max_length=100)
    categoria_id = models.IntegerField()
    nom_categoria = models.CharField(max_length=100)
    cod_negocio = models.IntegerField()
    nom_negocio = models.CharField(max_length=100)
    cod_linea = models.IntegerField()
    nom_linea = models.CharField(max_length=100)
    cod_marca = models.CharField(max_length=10)
    nom_marca = models.CharField(max_length=100)
    cod_articulo = models.DecimalField(max_digits=8, decimal_places=2)
    nom_articulo = models.CharField(max_length=100)
    dias_vencimiento = models.IntegerField()
    sku_devolucion = models.DecimalField(max_digits=8, decimal_places=2)
    sku_transito = models.DecimalField(max_digits=8, decimal_places=2)
    sku_no_apta = models.DecimalField(max_digits=8, decimal_places=2)
    sku_cantidad_total = models.DecimalField(max_digits=8, decimal_places=2)
    estibas = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'general_almacenamiento_sku'
