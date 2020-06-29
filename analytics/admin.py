from django.contrib import admin
from analytics.models import TypeBoard, Board, Comment


class TypeBoardAdmin(admin.ModelAdmin):
    fields = ['name', 'code']


class BoardAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'type', 'status', 'rol']
    list_display = ('name', 'description', 'type', 'created_at')


class CommentAdmin(admin.ModelAdmin):
    fields = ['message', 'user', 'board']
    list_display = ('message', 'user', 'board', 'created_at')


admin.site.register(TypeBoard, TypeBoardAdmin)
admin.site.register(Board, BoardAdmin)
admin.site.register(Comment, CommentAdmin)
