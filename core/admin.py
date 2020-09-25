from django.contrib import admin

from core.models import CategoriasBodegasDim, UploadTemplaCSV


class CategoryAdmin(admin.ModelAdmin):
    fields = ['nom_categoria']
    list_display = ['nom_categoria']


class TempletaCSVAdmin(admin.ModelAdmin):
    fields = ['file', 'company']
    list_display = ('file_name', 'company_name', 'created_at')

    def company_name(self, obj):
        return obj.company.name

    company_name.short_description = u'Compañia'

    def file_name(self, obj):
        return str(obj.file).split('/')[-1]

    file_name.short_description = u'Nombre Plantilla'



admin.site.register(CategoriasBodegasDim, CategoryAdmin)
admin.site.register(UploadTemplaCSV, TempletaCSVAdmin)