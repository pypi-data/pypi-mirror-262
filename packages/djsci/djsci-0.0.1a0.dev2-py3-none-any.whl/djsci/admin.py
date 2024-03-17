from django.contrib import admin

from .models import LocalNotebook, PrivateFile


class PrivateFileAdmin(admin.ModelAdmin):
    list_display = ("name", "id")


admin.site.register(PrivateFile, PrivateFileAdmin)


class LocalNotebookAdmin(admin.ModelAdmin):
    list_display = ("get_notebook_name", "id")
    ordering = ['notebook']

    def get_notebook_name(self, obj):
        return obj.notebook.name.rsplit('/')[-1].rsplit('.')[0]


admin.site.register(LocalNotebook, LocalNotebookAdmin)
