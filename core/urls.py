
from django.urls import include,path

from core import views
from .views import ReviewEmailView 


urlpatterns = [
    path('', views.index),
	# Students
	path('student/dashboard', views.dashboardStudent),
	path('student/profiles', views.profiles),
	path('student/prices', views.prices),
	path('student/personaldata', views.personaldata),
    path('reviews/', ReviewEmailView.as_view(), name="reviews"),

]
