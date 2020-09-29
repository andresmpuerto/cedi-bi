from django.core.validators import FileExtensionValidator
from django.db import models
from account.models import Company


def user_directory_path(instance, filename):
    return 'csv/data/company_{0}/{1}'.format(instance.company.id, filename)


class ErrorType(models.Model):
    name = models.CharField(max_length=20, verbose_name="Tipo de Error")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo de Errore"


class ErrorLog(models.Model):
    description = models.CharField(max_length=100, verbose_name="Descripción del Error")
    type = models.ForeignKey(ErrorType, models.PROTECT, verbose_name="Tipo de Error")
    code = models.IntegerField(verbose_name="Código de error")

    class Meta:
        verbose_name = "Tabla de Errore"


class Upload(models.Model):
    name = models.CharField(max_length=30, verbose_name="Nombre de Carga")
    file = models.FileField(upload_to=user_directory_path,
                            validators=[FileExtensionValidator(['csv'])],
                            verbose_name="Archivo .csv")
    min = models.IntegerField(default=1, verbose_name="Cantidad mínima de registros")
    max = models.IntegerField(default=10000, verbose_name="Camtidad Máxima de Registros")
    separator = models.CharField(default=';', max_length=1, verbose_name="Separador de datos")
    status = models.ForeignKey(ErrorLog, null=True, on_delete=models.PROTECT, editable=False)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name="Empresa")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False, verbose_name="Fecha de Carga")
    updated_at = models.DateTimeField(auto_now=True, blank=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Carga de Archivo"
