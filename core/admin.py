from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.

from core import models

# admin.site.register(models.UF)
# admin.site.register(models.Enrolment)
# admin.site.register(models.EnrolmentUF)
admin.site.register(models.ProfileRequirement)
# admin.site.register(models.Record)
admin.site.register(models.Requirement)
admin.site.register(models.Req_enrol)
admin.site.register(models.Upload)


class CareerInline(admin.TabularInline):
    model = models.Career
    fields = ["edita", "code", "active", "hours"]
    readonly_fields = ["edita", "name", "code", "hours"]
    extra = 0
    # es poden afegir "camps virtuals" (readonly) al admin amb funcions

    def edita(self, obj):
        return mark_safe("<a href='/admin/core/career/{}'>Edita el cicle: {}</a>".format(
            obj.id, obj.name))


class MPInline(admin.TabularInline):
    readonly_fields = ["edita", "code"]
    fields = ["edita", "code"]
    model = models.MP
    extra = 0

    def edita(self, obj):
        return mark_safe("<a href='/admin/core/mp/{}'>Edita el MP: {}</a>".format(obj.id, obj.name))


class UFInline(admin.TabularInline):
    fields = ["edita", "code"]
    readonly_fields = ["edita", "code"]
    model = models.UF
    extra = 0

    def edita(self, obj):
        return mark_safe("<a href='/admin/core/uf/{}'>Edita la UF: {}</a>".format(
            obj.id, obj.name))


class TermAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ["name", "start", "end", "active"]
    inlines = [CareerInline]


class CareerAdmin(admin.ModelAdmin):
    exclude = ()
    readonly_fields = ["name", "Enrera"]
    inlines = [MPInline]
    extra = 0

    def Enrera(self, obj):
        return mark_safe("<a href='/admin/core/term/{}/'>Retorna al curs: {}</a>".format(obj.term.id, obj.term.name))


class MpAdmin(admin.ModelAdmin):
    readonly_fields = ["Enrera"]
    list_display = ("name", "code",)
    search_fields = ("name", "code", "career__name")
    inlines = [UFInline]

    def Enrera(self, obj):
        return mark_safe("<a href='/admin/core/career/{}'>Retorna al cicle: {}</a>".format(obj.id, obj.career.name))


class UFAdmin(admin.ModelAdmin):
    readonly_fields = ["Enrera"]

    def Enrera(self, obj):
        return mark_safe("<a href='/admin/core/mp/{}'>Retorna al MP: {}</a>".format(obj.id, obj.mp.name))


class EnrolmentAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ["state", "email", "dni"]
    order_by = ["state"]


class Req_EnrolInline(admin.TabularInline):
  pass


admin.site.register(models.Term, TermAdmin)
admin.site.register(models.Career, CareerAdmin)
admin.site.register(models.MP, MpAdmin)
admin.site.register(models.UF, UFAdmin)
admin.site.register(models.Enrolment, EnrolmentAdmin)
