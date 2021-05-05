from django.shortcuts import render

def index (request):
    return render(request,"index.html", {'name':"Lollita"})

def login (request):
    return render(request,"login.html")


