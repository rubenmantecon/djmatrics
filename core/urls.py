
from django.urls import include,path

from core import views


urlpatterns = [
    path('', views.index),
	# Students
	path('student/profiles', views.profiles),
]
