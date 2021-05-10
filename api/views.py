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

    userinfofields = ['email','username','first_name','last_name']
    userinfo= {}

    for attr, value in user.__dict__.items():
        if attr in userinfofields:
            userinfo[attr] = value

    return Response(userinfo)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetProfilesAndRequirements(request):

    profilerequirements = ProfileRequirement.objects.all()
    requirements = Requirement.objects.all()

    profilesandrequirements = {}

    profilerequirementfields = ['id','name','description']
    requirementsfields = ['name','profile_id']
    
    for pr in profilerequirements:
        for attrpr, valuepr in pr.__dict__.items():
            if attrpr in profilerequirementfields:
                if attrpr == 'id':
                    id = valuepr
                    profilesandrequirements[id] = {}
                else:
                    profilesandrequirements[id][attrpr] = valuepr
    
    for r in requirements:
        for attrr, valuer in r.__dict__.items():
            if attrr in requirementsfields:
                if attrr == 'profile_id':
                    profile_id = valuer
                    if not 'requirements' in profilesandrequirements[profile_id].keys():
                        profilesandrequirements[profile_id]['requirements'] = []
                else:
                    profilesandrequirements[profile_id]['requirements'].append(valuer)


    return Response(profilesandrequirements)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetCareer(request):

    enrolment = Enrolment.objects.get(role_id=request.user.id)
    careerid = enrolment.career_id

    career = Career.objects.get(id=careerid)
    mps = MP.objects.filter(career_id=careerid)

    mpsid = []

    for mp in mps:
        mpsid.append(mp.id)

    ufs = UF.objects.filter(mp_id__in=mpsid)

    careermpsufs = {}

    careerinfofields = ['name','code','desc','hours','start','end']
    mpsinfofields = ['name','code','desc']
    ufsinfofields = ['id','name','code','desc'] 
    

    for attrc, valuec in career.__dict__.items():
        if attrc in careerinfofields:
            careermpsufs[attrc] = valuec
    if 'modules' not in careermpsufs.keys():
            careermpsufs['modules'] = {}


    for mp in mps:
        mpid = mp.id
        careermpsufs['modules'][mpid] = {}
        for attrmp, valuemp in mp.__dict__.items():
            if attrmp in mpsinfofields:
                careermpsufs['modules'][mpid][attrmp] = valuemp
    mpkeys = careermpsufs['modules'].keys()
    for mpkey in mpkeys:
        if 'ufs' not in careermpsufs['modules'][mpkey]:
            careermpsufs['modules'][mpkey]['ufs'] = {}
     


    for uf in ufs:
        mp_id = uf.mp_id
        ufid = uf.id
        careermpsufs['modules'][mp_id]['ufs'][ufid] = {}
        for attruf, valueuf in uf.__dict__.items():
            if attruf in ufsinfofields:
                careermpsufs['modules'][mp_id]['ufs'][ufid][attruf] = valueuf


    return Response(careermpsufs)
