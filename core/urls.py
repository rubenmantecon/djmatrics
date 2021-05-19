
from django.urls import include,path

from core import views


urlpatterns = [
    path('', views.index),
	# Students
	path('student/dashboard', views.dashboardStudent),
	path('student/profiles', views.profiles),
	path('student/prices', views.prices),
	path('student/showprices', views.showPrice),
	path('student/personaldata', views.personaldata),
]
