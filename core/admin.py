from django.contrib import admin

# Register your models here.

from core import models

admin.site.register(models.Career)
admin.site.register(models.UF)
admin.site.register(models.Enrolment)


class MpAdmin(admin.ModelAdmin):
    list_display = ("name","code")
    search_fields= ("name","code","career__name")
    

admin.site.register(models.MP, MpAdmin)

