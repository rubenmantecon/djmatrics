from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.

from core import models

admin.site.register(models.UF)
admin.site.register(models.Enrolment)
#admin.site.register(models.EnrolmentUF)
admin.site.register(models.ProfileRequirement)
#admin.site.register(models.Record)
admin.site.register(models.Requirement)
admin.site.register(models.Req_enrol)
admin.site.register(models.Upload)

class CareerInline(admin.TabularInline):
	model = models.Career
	fields = ["name","code","active","edita","hours"]
	readonly_fields = ["edita","name","code","hours"]
	extra = 0
	# es poden afegir "camps virtuals" (readonly) al admin amb funcions
	def edita(self,obj):
		return mark_safe("<a href='/admin/core/career/{}'>{}</a>".format(
					obj.id,obj.name))

class TermAdmin(admin.ModelAdmin):
	exclude = ()
	list_display = ["name","start","end","active"]
	order_by = ["active",]
	inlines = [CareerInline,]

class CareerAdmin(admin.ModelAdmin):
	exclude = ()
	readonly_fields = ["back"]
	def back(self,obj):
		return mark_safe("<a href='/admin/core/term/{}'>\
			Retorna al curs: {}</a>".format(obj.id,obj.term.name))

class MpAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code", "career__name")


admin.site.register(models.Term, TermAdmin)
admin.site.register(models.Career, CareerAdmin)
admin.site.register(models.MP, MpAdmin)

