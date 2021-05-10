from django.shortcuts import render, HttpResponseRedirect
from django.core.exceptions import ValidationError
from .models import ProfileRequirement, Requirement, Enrolment
from .forms import SaveProfiles

def index (request):
    return render(request, "base.html", {'title':"INS Institut Esteve Terradas i Illa", 'user': "Enric"})

def login (request):
    return render(request,"login.html")

#@login_required
def dashboardStudent (request):
	return render(request, "student/dashboard.html", {'title': 'Dashboard | Matriculacions - INS Institut Esteve Terradas i Illa'});

#@login_required
def profiles (request):
	if request.method == 'POST':
		form = SaveProfiles(request.POST)
		if form.is_valid():
			if int(form.data['drets_imatge']) in [0, 1] and int(form.data['salides_excursio']) in [0, 1] and int(form.data['salides_extra']) in [0, 1]:
				
				if not Enrolment.objects.filter(role_id=request.user.id).exists():
					toSaveEnrolment = Enrolment.objects.create(
						role_id = request.user.id,
						image_rights = int(form.data['drets_imatge']),
						extracurricular = int(form.data['salides_extra']),
						excursions = int(form.data['salides_excursio']),
						state = 'Empty'
					)
				else:
					toSaveEnrolment = Enrolment.objects.get(role_id=request.user.id)
					toSaveEnrolment.image_rights = int(form.data['drets_imatge'])
					toSaveEnrolment.extracurricular = int(form.data['salides_extra'])
					toSaveEnrolment.excursions = int(form.data['salides_excursio'])

				if len(form.data) == 5:
					toSaveEnrolment.profile_id = int(form.data['profile'])
				else:
					toSaveEnrolment.profile_id = ''
				
				toSaveEnrolment.save()
				return HttpResponseRedirect('/student/prices')

	else:
		form = SaveProfiles()

	return render(request, 'student/profiles.html', {
		'title': 'Perfils d\'usuari | Matriculacions - INS Institut Esteve Terradas i Illa',
		'profiles': ProfileRequirement.objects.all(),
		'requirements': Requirement.objects.all(),
	});
	
#@login_required
def prices (request):
	return render(request, 'student/prices.html')

