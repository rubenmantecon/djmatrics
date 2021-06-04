from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.

from core import models
from django.contrib.auth.models import User


from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)


class EnrolmentInline(admin.TabularInline):
    model = models.Enrolment
    fields = ('first_name','last_name_1','last_name_2','ID_num','go_to_enrolment')
    readonly_fields = ('first_name','last_name_1','last_name_2','ID_num','go_to_enrolment')
    extra = 0
    def go_to_enrolment(self, obj):
        return mark_safe("<a href='/admin/core/enrolment/{}/'>Ves a la matricula</a>".format(obj.id))
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(User)
class MyUserAdmin(UserAdmin):
    ordering = ('-is_staff','last_name')
    inlines = [EnrolmentInline,]



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


class Req_EnrolInline(admin.TabularInline):
    fields = ["requirement", "enrolment", "state", "pujades"]
    readonly_fields = ["requirement", "pujades"]
    model = models.Req_enrol
    extra = 0

    def pujades(self, obj):
        html = """  """
        files = obj.upload_set.all()
        for upload in files:
            html += "<p><a href='/media/{}' target='_blank'>{}</a></p>".format(upload.data, upload.data)

        return mark_safe(html)


class TermAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ["name", "start", "end", "active"]
    inlines = [CareerInline]


class CareerAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ['name','term']
    readonly_fields = ["name", "Enrera"]
    inlines = [MPInline]
    extra = 0

    def Enrera(self, obj):
        return mark_safe("<a href='/admin/core/term/{}/'>Retorna al curs: {}</a>".format(obj.term.id, obj.term.name))


class MpAdmin(admin.ModelAdmin):
    readonly_fields = ["Enrera"]
    list_display = ("name", "code",'career','term')
    search_fields = ("name", "code", "career__name",'career__term__name')
    inlines = [UFInline]
    def term(self,obj):
        return obj.career.term.name
    def Enrera(self, obj):
        return mark_safe("<a href='/admin/core/career/{}'>Retorna al cicle: {}</a>".format(obj.id, obj.career.name))


class UFAdmin(admin.ModelAdmin):
    readonly_fields = ["Enrera"]
    search_fields = ['name','mp__name','mp__career__name']
    list_display = ['name','mp','cicle','course','active']
    list_editable = ['course',]
    ordering = ['mp__career__name','mp__name','name']
    def mp(self,obj):
        return obj.mp.name
    def cicle(self,obj):
        return obj.mp.career.name
    def Enrera(self, obj):
        return mark_safe("<a href='/admin/core/mp/{}'>Retorna al MP: {}</a>".format(obj.id, obj.mp.name))


@admin.register(models.Enrolment)
class EnrolmentAdmin(admin.ModelAdmin):
    exclude = ()
    save_on_top = True
    search_fields = ["career__name", "ID_num","email",'first_name','last_name_1','last_name_2']
    #list_filter = ["career__name"]
    list_display = ["state","documents_pujats", "nom", "email", "ID_num","career" ]
    readonly_fields = ["Enrera"]
    order_by = ["state"]
    inlines = [Req_EnrolInline]
    filter_horizontal = ('ufs',)
    def formfield_for_manytomany(self, db_field, request, *args, **kwargs):
        if db_field.name == "ufs":
            object_id = request.resolver_match.kwargs['object_id']
            enrolment = models.Enrolment.objects.get(pk=object_id)
            if enrolment.career:
                kwargs["queryset"] = models.UF.objects.filter(
                                        mp__career__code=enrolment.career.code)
            else:
                kwargs["queryset"] = models.UF.objects.none()
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    def nom(self,obj):
        return "{} {}, {}".format(obj.last_name_1,obj.last_name_2,obj.first_name)
    def Enrera(self, obj):
        return mark_safe("<a href='/admin/core/enrolment'>Retorna al llistat de matrícules</a>")
    # TODO: falta hacer una query que me mire si todos los req_enrols de un enrolment están subidos Y validados como confirmados. Además, esta función tiene que ejecutarse cada vez que hay un cambio en los req_enrol de dicho enrolment.

class Req_EnrolAdmin(admin.ModelAdmin):
    fields = ["enrolment", "requirement", "state"]
    model = models.Req_enrol


class RequirementAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ["name", "profile"]
    model = models.Requirement


class RequirementInline(admin.TabularInline):
    model = models.Requirement
    extra = 1

@admin.register(models.ProfileRequirement)
class ProfileRequirementAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ("name","profile_type")
    inlines = [RequirementInline,]





admin.site.register(models.Term, TermAdmin)
admin.site.register(models.Career, CareerAdmin)
admin.site.register(models.MP, MpAdmin)
admin.site.register(models.UF, UFAdmin)
admin.site.register(models.Requirement, RequirementAdmin)
admin.site.register(models.Upload)
admin.site.register(models.Req_enrol)
