from django.urls import path
from rest_framework import routers

from . import views

route = routers.DefaultRouter()

urlpatterns = route.urls

urlpatterns += path('token', views.GetAccessToken),
urlpatterns += path('user', views.GetUserInfo),
urlpatterns += path('profilesandrequirements', views.GetProfilesAndRequirements),