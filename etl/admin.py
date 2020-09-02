from django.contrib import admin
from etl.models import Upload, ErrorLog, ErrorType
import etl.transform.validate as validate
import etl.load.dimension as dim
import etl.load.fact as fact
from django.conf import settings


class ErrorTypeAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name']


class ErrorLogAdmin(admin.ModelAdmin):
    fields = ['description', 'type', 'code']
    list_display = ('code', 'description')


class UploadAdmin(admin.ModelAdmin):
    fields = ['name', 'file', 'min', 'max', 'separator', 'company']
    list_display = ('name', 'company_nit', 'status_code', 'status_type', 'status_description', 'created_at')

    def company_nit(self, obj):
        return obj.company.nit

    def status_code(self, obj):
        return obj.status.code

    def status_type(self, obj):
        return obj.status.type.name

    def status_description(self, obj):
        return obj.status.description

    def save_model(self, request, obj, form, change):
        super(UploadAdmin, self).save_model(request, obj, form, change)
        # TODO copiar codigo Diego
        code = self.validate_file(obj)
        if code is 0:
            self.create_dimensions(obj)
            self.create_fact(obj)

        status = ErrorLog.objects.get(code=code)
        self.update_status(obj.id, status)

    def update_status(self, pk, status):
        up = Upload.objects.get(pk=pk)
        up.status = status
        up.save()

    def validate_file(self, obj):
        # VALIDACIONES DE ARCHIVO
        val = validate.ValidateCsv(str(settings.ROOT_DIR)+'\\'+str(obj.file), obj.separator, obj.min, obj.max)
        # Validación 1: valida el separador del archivo
        if val.is_separator() is False:
            return 1002  # separador icorrecto
        # Validación 2: valida el numero de filas: 10001>filas>0
        if val.has_correct_size() is False:
            return 1003  # cntidad de registros nocumple
        # Validación 3: valida la cantidad, ORDEN Y NOMBRES de columnas  contra el archivo plantilla
        if val.has_template(str(settings.ROOT_DIR)+'\\csv\\template.csv') is False:
            return 1004  # columnas incorrectas
        # Validación 4: valida datos nulos
        if val.is_null() is False:
            return 1005

        return 0

    def create_dimensions(self, obj):
        dimension = dim.Dimensions(str(settings.ROOT_DIR)+'\\'+str(obj.file),
                                   obj.separator,
                                   [settings.DATABASES['default']['USER'],
                                    settings.DATABASES['default']['PASSWORD'],
                                    settings.DATABASES['default']['HOST'],
                                    settings.DATABASES['default']['NAME']])
        dimension.dim_bodegas()
        dimension.dim_negocios()
        dimension.dim_lineas()
        dimension.dim_marcas()
        dimension.dim_articulos()
        dimension.dim_lotes()

    def create_fact(self, obj):
        table = fact.Fact(str(settings.ROOT_DIR)+'\\'+str(obj.file),
                          obj.separator,
                          [settings.DATABASES['default']['USER'],
                           settings.DATABASES['default']['PASSWORD'],
                           settings.DATABASES['default']['HOST'],
                           settings.DATABASES['default']['NAME']])
        table.cedibi_fact()


admin.site.register(ErrorType, ErrorTypeAdmin)
admin.site.register(ErrorLog, ErrorLogAdmin)
admin.site.register(Upload, UploadAdmin)
