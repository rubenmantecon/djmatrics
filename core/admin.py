from django.contrib import admin

# Register your models here.

from core import models

admin.site.register(models.Career)
admin.site.register(models.UF)
admin.site.register(models.Term)
admin.site.register(models.Enrolment)
#admin.site.register(models.EnrolmentUF)
admin.site.register(models.ProfileRequirement)
#admin.site.register(models.Record)
admin.site.register(models.Requirement)
#admin.site.register(models.Req_enrol)
#admin.site.register(models.Upload)

class MpAdmin(admin.ModelAdmin):
    list_display = ("name","code")
    search_fields= ("name","code","career__name")


admin.site.register(models.MP, MpAdmin)

