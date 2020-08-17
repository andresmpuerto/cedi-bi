from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    document_type = models.CharField(max_length=2)
    document_id = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True, editable=False)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Rol(models.Model):
    name = models.CharField(max_length=20)
    code = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Role"


def user_directory_path(instance, filename):
    return 'images/company_{0}/{1}'.format(instance.nit, filename)


class Company(models.Model):
    name = models.CharField(max_length=50)
    nit = models.CharField(max_length=9)
    logo = models.ImageField(upload_to=user_directory_path)
    description = models.CharField(max_length=9)
    status = models.BooleanField(default=True)
    contact_name = models.CharField(max_length=30)
    contact_email = models.CharField(max_length=40)
    contact_phone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Compañia"


class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    phone = models.CharField(max_length=12)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, blank=True, editable=False)

    def __str__(self):
        return self.user.first_name + " (" + self.rol.name + ")"

    class Meta:
        verbose_name = "Perfil de Usuario"
