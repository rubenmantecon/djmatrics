from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import ProfileRequirement, Req_enrol, Requirement, Enrolment, User
from .forms import SaveProfiles

def index (request):
    return render(request, "base.html", {'title':"INS Institut Esteve Terradas i Illa", 'user': "Enric"})

@login_required
def dashboardStudent (request):
	documentsQuery = Req_enrol.objects.filter(enrolment_id=request.user.id)

	documents = []
	count = 0
	for document in documentsQuery:
		documents.append([])
		documents[count].append(Requirement.objects.get(id=document.requirement_id).name)
		documents[count].append(document.state)

		count += 1

	return render(request, "student/dashboard.html", {
		'title': 'Dashboard | Matriculacions - INS Institut Esteve Terradas i Illa', 
		'breadcrumb': [{'link': '/student/dashboard', 'text': 'Inici'},{'link': '#', 'text': 'Dashboard'}],
		'enrolmentStatus': Enrolment.objects.get(id=request.user.id).state,
		'documents': documents,
		}
	);

@login_required
def personaldata (request):
	'''params = {
		'first_name': User.objects.get(id=)
	}'''


	return render(request, 'student/personaldata.html', {
		'title': 'Data personal | Matriculacions - INS Institut Esteve Terradas i Illa',
		'requirements': Requirement.objects.all(),
		'breadcrumb': [{'link': '/student/dashboard', 'text': 'Inici'},{'link': '#', 'text': 'Alumne'},{'link': '/student/personaldata', 'text': 'Data personal'}]
	});

@login_required
def login (request):
    return render(request, "account/login.html")

@login_required
def profiles (request):
	if request.method == 'POST':
		form = SaveProfiles(request.POST)
		if form.is_valid():
			if int(form.data['drets_imatge']) in [0, 1] and int(form.data['salides_excursio']) in [0, 1] and int(form.data['salides_extra']) in [0, 1]:
				
				if not Enrolment.objects.filter(id=request.user.id).exists():
					toSaveEnrolment = Enrolment.objects.create(
						id = request.user.id,
						image_rights = int(form.data['drets_imatge']),
						extracurricular = int(form.data['salides_extra']),
						excursions = int(form.data['salides_excursio']),
						state = 'P'
					)
				else:
					toSaveEnrolment = Enrolment.objects.get(id=request.user.id)
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
		'breadcrumb': [{'link': '/student/dashboard', 'text': 'Inici'},{'link': '#', 'text': 'Matriculació'},{'link': '/student/profiles', 'text': 'Perfils'}]
	});
	
@login_required
def prices (request):
	return render(request, 'student/prices.html',
		{'breadcrumb': [{'link': '/student/dashboard', 'text': 'Inici'},{'link': '#', 'text': 'Matriculació'},{'link': '/student/prices', 'text': 'Preu'}]}
	)