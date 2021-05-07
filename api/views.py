from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from django.contrib.auth.models import User
from core.models import *
from django.contrib.auth.hashers import check_password

@api_view(['POST'])
def GetAccessToken(request):
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({ detail: "No s'ha trobat l'usuari" })
    
    pwd_valid = check_password(password,user.password)

    if not pwd_valid:
        return Response({ detail: "Contrasenya incorrecta" })
    
    token, created = Token.objects.get_or_create(user=user)

    return Response({ "Token": token.key })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserInfo(request):
    
    user = User.objects.get(id=request.user.id)

    UserInfoFields = ['email','username','first_name','last_name']
    UserInfo= {}

    for attr, value in user.__dict__.items():
        if attr in UserInfoFields:
            UserInfo[attr] = value

    return Response(UserInfo)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetProfilesAndRequirements(request):

    ProfileRequirements = ProfileRequirement.objects.all()
    Requirements = Requirement.objects.all()

    ProfilesAndRequirements = {}

    ProfileRequirementFields = ['id','name','description']
    RequirementsFields = ['name','profile_id']
    
    for PR in ProfileRequirements:
        for attrPR, valuePR in PR.__dict__.items():
            if attrPR in ProfileRequirementFields:
                if attrPR == 'id':
                    id = valuePR
                    ProfilesAndRequirements[id] = {}
                else:
                    ProfilesAndRequirements[id][attrPR] = valuePR
    
    for R in Requirements:
        for attrR, valueR in R.__dict__.items():
            if attrR in RequirementsFields:
                if attrR == 'profile_id':
                    profile_id = valueR
                    if not 'requirements' in ProfilesAndRequirements[profile_id].keys():
                        ProfilesAndRequirements[profile_id]['requirements'] = []
                else:
                    ProfilesAndRequirements[profile_id]['requirements'].append(valueR)


    return Response(ProfilesAndRequirements)