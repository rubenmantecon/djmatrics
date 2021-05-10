from django.shortcuts import render

def index (request):
    return render(request, "base.html", {'title':"INS Institut Esteve Terradas i Illa", 'user': "Enric"})

def login (request):
    return render(request,"login.html")

#@login_required
def profiles (request):
	return render(request, "student/profiles.html", {'title': 'Perfils d\'usuari | Matriculacions - INS Institut Esteve Terradas i Illa'});
