from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import user_passes_test
from .models import *
from .forms import SaveProfiles
from django.contrib import messages
from core.compute_price import compute_price


""" {
	'careerComplete': false,
	'UFs': ['4','4','5']
} """

def index (request):
    return render(request, "landingpage.html", {'title':"INS Institut Esteve Terradas i Illa", 'user': "Enric"})

@login_required
def dashboardStudent (request):
	documentsQuery = Req_enrol.objects.filter(enrolment_id=request.user.id)

	# If the user doesn't have an enrolment will be redirected to the wizard
	try:
		enrolmentUser = Enrolment.objects.get(id=request.user.id)
	except Enrolment.DoesNotExist:
		return HttpResponseRedirect('/student/profiles')
		
	if enrolmentUser.image_rights is None or enrolmentUser.excursions is None or enrolmentUser.extracurricular is None:
		messages.add_message(request, messages.INFO, 'Hem detectat que necessites seleccionar les autoritzacions.')
		return HttpResponseRedirect('/student/profiles')

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
		'enrolmentStatus': enrolmentUser.state,
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

	if request.method == 'POST':
		if request.POST["data-perfect"] == '1':
			messages.add_message(request, messages.SUCCESS, 'Has confirmat les teves dades.')
			return HttpResponseRedirect('/student/dashboard')



	return render(request, 'student/personaldata.html', {
		'title': 'Data personal | Matriculacions - INS Institut Esteve Terradas i Illa',
		'requirements': Requirement.objects.all(),
		'params': params,
		'breadcrumb': [{'link': '/student/dashboard', 'text': 'Inici'},{'link': '#', 'text': 'Alumne'},{'link': '/student/personaldata', 'text': 'Dades personals'}]
	});

@user_passes_test(lambda u: u.is_anonymous)
def login (request):
    return render(request, "account/login.html")

@login_required
def profiles (request):
	if request.method == 'POST':
		form = SaveProfiles(request.POST)
		if form.is_valid():
			if int(form.data['drets_imatge']) in [0, 1] and int(form.data['salides_excursio']) in [0, 1] and int(form.data['salides_extra']) in [0, 1]:
				
				if not Enrolment.objects.filter(user=request.user).exists():
					toSaveEnrolment = Enrolment.objects.create(
						user = request.user,
						image_rights = int(form.data['drets_imatge']),
						extracurricular = int(form.data['salides_extra']),
						excursions = int(form.data['salides_excursio']),
						state = 'P'
					)
				else:
					toSaveEnrolment = Enrolment.objects.get(user=request.user)
					toSaveEnrolment.image_rights = int(form.data['drets_imatge'])
					toSaveEnrolment.extracurricular = int(form.data['salides_extra'])
					toSaveEnrolment.excursions = int(form.data['salides_excursio'])

				if form.data.get('profile'):
					toSaveEnrolment.profile_id = int(form.data['profile'])
				else:
					toSaveEnrolment.profile_id = ''
				
				toSaveEnrolment.save()
				messages.add_message(request, messages.SUCCESS, 'S\'ha desat les dades.')
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
	enrolmentUser = request.user.enrolment

	if enrolmentUser.image_rights is None or enrolmentUser.excursions is None or enrolmentUser.extracurricular is None:
		messages.add_message(request, messages.INFO, 'Hem detectat que necessites seleccionar les autoritzacions.')
		return HttpResponseRedirect('/student/profiles')

	return render(request, 'student/prices.html',
		{
			'breadcrumb': [{'link': '/student/dashboard', 'text': 'Inici'},{'link': '#', 'text': 'Matriculació'},{'link': '/student/prices', 'text': 'Preu'}],
			'title': 'Calculació del preu | Matriculacions - INS Institut Esteve Terradas i Illa',
			'enrolment': enrolmentUser,
		},
	)

@login_required
def showPrice (request):
	if request.method == 'POST':
		enrolment = request.user.enrolment
		print(request.POST)
		enrolment.uf.clear()
		for i in range(0,100):
			if request.POST.get('uf-'+str(i)):
				uf = request.POST['uf-'+str(i)]
				print('Uf sola: ' + uf)
				enrolment.uf.add(uf)
			
		enrolment.save()
		totalPrice = compute_price(enrolment)
		
		return render(request, 'student/show_price.html',
			{
				'breadcrumb': [{'link': '/student/dashboard', 'text': 'Inici'},{'link': '#', 'text': 'Matriculació'},{'link': '/student/showprices', 'text': 'Preu'}],
				'title': 'Calculació del preu | Matriculacions - INS Institut Esteve Terradas i Illa',
				'price': totalPrice,
			},
		)
	else:
		messages.add_message(request, messages.ERROR, 'No tens permisos per a accedir a aquesta pàgina.')
		return HttpResponseRedirect('/student/prices')