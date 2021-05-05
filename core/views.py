from django.shortcuts import render

def index (request):
    return render(request, "base.html", {'title':"INS Institut Esteve Terradas i Illa", 'user': "Enric"})

#@login_required
def profiles (request):
	return render(request, "student/profiles.html", {'title': 'Perfils d\'usuari | Matriculacions - INS Institut Esteve Terradas i Illa'});
