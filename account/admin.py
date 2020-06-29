from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Rol, Company, Profile, User


class RolAdmin(admin.ModelAdmin):
    fields = ['name', 'code']


class CompanyAdmin(admin.ModelAdmin):
    fields = ['name', 'nit', 'logo', 'description', 'status']
    list_display = ('nit', 'name', 'status', 'created_at')


class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'rol', 'phone', 'company', 'active']


admin.site.register(User, UserAdmin)
admin.site.register(Rol, RolAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Profile, ProfileAdmin)
