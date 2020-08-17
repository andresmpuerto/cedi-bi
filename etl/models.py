from django.core.validators import FileExtensionValidator
from django.db import models
from account.models import Company


def user_directory_path(instance, filename):
    return 'csv/company_{0}/{1}'.format(instance.company.id, filename)


class ErrorType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tipo de Errore"


class ErrorLog(models.Model):
    description = models.CharField(max_length=100)
    type = models.ForeignKey(ErrorType, models.PROTECT)
    code = models.IntegerField()

    class Meta:
        verbose_name = "Tabla de Errore"


class Upload(models.Model):
    name = models.CharField(max_length=30)
    file = models.FileField(upload_to=user_directory_path, validators=[FileExtensionValidator(['csv'])])
    min = models.IntegerField(default=1)
    max = models.IntegerField(default=10000)
    separator = models.CharField(default=';', max_length=1)
    status = models.ForeignKey(ErrorLog, null=True, on_delete=models.PROTECT, editable=False)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Carga de Archivo"
