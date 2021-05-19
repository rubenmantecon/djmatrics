from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from .models import ProfileRequirement, Req_enrol, Requirement, Enrolment, User
from .forms import SaveProfiles, ReviewForm
from django.views.generic.edit import FormView


class ReviewEmailView(FormView):
    template_name="review.html"
    form_class=ReviewForm

    def form_valid(self, form):
        form.send_mail()
        msg = "Thanks for the review"
        return HttpResponse(msg)

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
	params = [
		["Nom de l’usuari", request.user.first_name],
		["Cognoms de l'usuari", request.user.last_name],
		["Correu electrònic", request.user.email],
	]

	userEnrolment = Enrolment.objects.get(id=request.user.id)
	if userEnrolment:
		paramsEnrolment = [
			["Document nacional d'identitat", userEnrolment.dni],
			["Data de naixement", userEnrolment.birthday],
			["Localització de naixement", userEnrolment.birthplace],
			["Adreça", userEnrolment.address],
			["Ciutat", userEnrolment.city],
			["Codi postal", userEnrolment.postal_code],
			["Telefon mòbil", userEnrolment.phone_number],
			["Telefon d'emergència", userEnrolment.emergency_number],
			["Tutor 1 - Document nacional d'identitat", userEnrolment.tutor_1_dni],
			["Tutor 1 - Nom complet", "{} {} {}".format(userEnrolment.tutor_1_name, userEnrolment.tutor_1_lastname1, userEnrolment.tutor_1_lastname2)],
			["Tutor 2 - Document nacional d'identitat", userEnrolment.tutor_2_dni],
			["Tutor 2 - Nom complet", "{} {} {}".format(userEnrolment.tutor_2_name, userEnrolment.tutor_2_lastname1, userEnrolment.tutor_2_lastname2)],
		]

		for param in paramsEnrolment:
			params.append(param)


	return render(request, 'student/personaldata.html', {
		'title': 'Data personal | Matriculacions - INS Institut Esteve Terradas i Illa',
		'requirements': Requirement.objects.all(),
		'params': params,
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
		'profilesBonus': ProfileRequirement.objects.filter(profile_type='bonificació del 50%'),
		'profilesExemption': ProfileRequirement.objects.filter(profile_type='exempció'),
		'profilesMandatory': ProfileRequirement.objects.filter(profile_type='obligatori'),
		'requirements': Requirement.objects.all(),
		'breadcrumb': [{'link': '/student/dashboard', 'text': 'Inici'},{'link': '#', 'text': 'Matriculació'},{'link': '/student/profiles', 'text': 'Perfils'}]
	});
	
@login_required
def prices (request):
	return render(request, 'student/prices.html',
		{'breadcrumb': [{'link': '/student/dashboard', 'text': 'Inici'},{'link': '#', 'text': 'Matriculació'},{'link': '/student/prices', 'text': 'Preu'}]}
	)