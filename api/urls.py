from django.urls import path
from rest_framework import routers

from . import views

route = routers.DefaultRouter()

urlpatterns = route.urls

urlpatterns += path('token', views.GetAccessToken),
urlpatterns += path('user', views.GetUserInfo),
urlpatterns += path('profilesandrequirements', views.GetProfileAndRequirements),
urlpatterns += path('career', views.GetCareer),
urlpatterns += path('imagerights', views.GetImageRights),
urlpatterns += path('check', views.VerifyToken),