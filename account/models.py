from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    document_type = models.CharField(max_length=2, verbose_name="Tipo de Documento")
    document_id = models.CharField(max_length=15, verbose_name="Docuemnto de Identidad")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, blank=True, editable=False)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Rol(models.Model):
    name = models.CharField(max_length=20, verbose_name="Nombre del Rol")
    code = models.IntegerField(verbose_name="Código de Rol")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Role"


def user_directory_path(instance, filename):
    return 'images/company_{0}/{1}'.format(instance.nit, filename)


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre de Compañia")
    nit = models.CharField(max_length=9, verbose_name="N.I.T.")
    logo = models.ImageField(upload_to=user_directory_path, verbose_name="Logo de la Compañia")
    description = models.CharField(max_length=50, verbose_name="Actividad Económíca")
    status = models.BooleanField(default=True, verbose_name="Activo")
    contact_name = models.CharField(max_length=30, verbose_name="Nombre de Contacto")
    contact_email = models.CharField(max_length=40, verbose_name="Email de contacto")
    contact_phone = models.CharField(max_length=30, verbose_name="Celular de Contacto")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, blank=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Compañia"


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE, verbose_name="Usuario")
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, verbose_name="Rol de Usuario")
    phone = models.CharField(max_length=12, verbose_name="Número Celular")
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name="Compañia")
    active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, blank=True, editable=False)

    def __str__(self):
        return self.user.first_name + " (" + self.rol.name + ")"

    class Meta:
        verbose_name = "Perfil de Usuario"
