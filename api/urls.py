from django.urls import path
from rest_framework import routers

from . import views

route = routers.DefaultRouter()

urlpatterns = route.urls

urlpatterns += path('verify', views.VerifyToken),
urlpatterns += path('token', views.GetAccessToken),
urlpatterns += path('updatewizard', views.UpdateWizard),
urlpatterns += path('getwizard', views.GetWizard),
urlpatterns += path('getreqstatus', views.GetRequirementStatus),
urlpatterns += path('user', views.GetUserInfo),
urlpatterns += path('profileandrequirements', views.GetProfileAndRequirements),
urlpatterns += path('profilesandrequirements', views.GetProfilesAndRequirements),
urlpatterns += path('career', views.GetCareer),
urlpatterns += path('uploadreq', views.UploadReqFiles),