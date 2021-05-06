from django.shortcuts import render
from .models import ProfileRequirement, Requirement
# from .forms import SaveProfiles

def index (request):
    return render(request, "base.html", {'title':"INS Institut Esteve Terradas i Illa", 'user': "Enric"})

#@login_required
def dashboardStudent (request):
	return render(request, "student/dashboard.html", {'title': 'Dashboard | Matriculacions - INS Institut Esteve Terradas i Illa'});

#@login_required
def profiles (request):
	#form = PostForm()
	return render(request, 'student/profiles.html', {
		'title': 'Perfils d\'usuari | Matriculacions - INS Institut Esteve Terradas i Illa',
		'profiles': ProfileRequirement.objects.all(),
		'requirements': Requirement.objects.all(),
	});

