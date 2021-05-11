
from django.urls import include,path

from core import views


urlpatterns = [
    path('', views.index),
	# Students
	path('student/dashboard', views.dashboardStudent),
	path('accounts/login', views.login),
	path('student/profiles', views.profiles),
	path('student/prices', views.prices)
]
