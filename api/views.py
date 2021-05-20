from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from django.contrib.auth.models import User
from core.models import *
from django.contrib.auth.hashers import check_password



@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def VerifyToken(request):
    
    userid = request.headers['UID']
    tokenid = request.headers['Token']
    
    try:
        token = Token.objects.get(user_id=userid,key=tokenid)
        authbool = True
    except Token.DoesNotExist:
        authbool = False
    
    return Response(authbool,status=200)


@api_view(['POST'])
def GetAccessToken(request):

    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = User.objects.get(email=email, is_superuser=0, is_staff=0)
    except User.DoesNotExist:
        return Response({ 'detail': "No s'ha trobat l'usuari" }, status=401)
    
    pwd_valid = check_password(password,user.password)

    if not pwd_valid:
        return Response({ 'detail': "Contrasenya incorrecta" }, status=401)
    
    try:
        Token.objects.get(user=user).delete()
        token = Token.objects.create(user=user)
    except Token.DoesNotExist:
        token = Token.objects.create(user=user)

    enrolment = Enrolment.objects.get(user_id=user.id)

    return Response({ 'Token': token.key, 'StatusEnrolment': enrolment.state, 'BoolWizard': True if enrolment.profile_req_id else False, 'UserId': user.id },status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def UpdateWizard(request):

    enrolment = Enrolment.objects.get(user_id=request.user.id)
    beforeprofileid = enrolment.profile_req_id
    
    for key, value in request.POST.items():
        value = value.lower()
        if key == 'ImageRights':
            enrolment.image_rights = True if value == 'true' else False
        elif key == 'Excursions':
            enrolment.excursions = True if value == 'true' else False
        elif key == 'Extracurriculars':
            enrolment.extracurricular = True if value == 'true' else False
        elif key == 'Profile': 
            if value == 'standard':
                enrolment.profile_req_id = 1
            elif value == 'bonus':
                enrolment.profile_req_id = 2
            elif value == 'exception':
                enrolment.profile_req_id = 3
            sameprofile = True if enrolment.profile_req_id == beforeprofileid else False
    
    enrolment.save()

    if sameprofile == False:
        enrolment = Enrolment.objects.get(user_id=request.user.id)
        reqenrol = Req_enrol.objects.filter(enrolment_id=enrolment.id)
        
        reqenrolids = []

        for rq in reqenrol:
            reqenrolids.append(rq.id)
        
        uploads = Upload.objects.filter(req_enrol_id__in=reqenrolids)
        uploads.delete()

        reqenrol.delete()
        
        requirements = Requirement.objects.filter(profile_id=enrolment.profile_req_id)

        for requirement in requirements:
            Req_enrol.objects.create(state='B', enrolment_id=enrolment.id, requirement_id=requirement.id)
    
    return Response(status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetWizard(request):

    enrolment = Enrolment.objects.get(user_id=request.user.id)
    enrolmentinfofields = ['image_rights','excursions','extracurricular']

    wizard = {}

    for attr, value in enrolment.__dict__.items():
        if attr in enrolmentinfofields:
            wizard[attr] = value
        
    return Response(wizard,status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetRequirementStatus(request):

    enrolment = Enrolment.objects.get(user_id=request.user.id)
    reqenrols = Req_enrol.objects.filter(enrolment_id=enrolment.id)

    requirementstatus = {}

    for reqenrol in reqenrols:
        requirementstatus[reqenrol.requirement_id] = reqenrol.state
    
    return Response(requirementstatus,status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetUserInfo(request):
    
    user = User.objects.get(id=request.user.id)
    enrolment = Enrolment.objects.get(user_id=user.id)

    userinfofields = ['username','first_name','last_name','email']
    enrolmentinfofields = ['dni','birthplace','birthday','address','city','postal_code','phone_number','emergency_number','tutor_1','tutor_2']

    userinfo= {}

    for attr, value in user.__dict__.items():
        if attr in userinfofields:
            userinfo[attr] = value
    
    for attr, value in enrolment.__dict__.items():
        if attr in enrolmentinfofields:
            userinfo[attr] = value

    return Response(userinfo,status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetProfileAndRequirements(request):
        
    enrolment = Enrolment.objects.get(user_id=request.user.id)
    profilerequirement = ProfileRequirement.objects.get(id=enrolment.profile_req_id)
    requirements = Requirement.objects.filter(profile_id=profilerequirement.id)

    profileandrequirements = { "Name":  profilerequirement.name , "Description": profilerequirement.description , "Type": profilerequirement.profile_type, "Requirements": {} }

    for requirement in requirements:
        profileandrequirements['Requirements'][requirement.id] = requirement.name
    
    return Response(profileandrequirements,status=200)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetProfilesAndRequirements(request):

    profilerequirements = ProfileRequirement.objects.all()
    requirements = Requirement.objects.all()

    profilesandrequirements = {}

    profilerequirementfields = ['id','name','description','profile_type']
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

    return Response(profilesandrequirements,status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetCareer(request):

    enrolment = Enrolment.objects.get(user_id=request.user.id)
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

    return Response(careermpsufs,status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([FileUploadParser])
def UploadReqFiles(request, format=None):
    
    reqenrol = Req_enrol.objects.filter(enrolment_id=request.user.id)
        
    reqenrolids = []

    for rq in reqenrol:
        if rq.state != 'V':
            reqenrolids.append(rq.id)
    if 'file' not in request.data:
        return Response("no data")

    uploads = Upload.objects.filter(req_enrol_id__in=reqenrolids)
    uploads.delete()
    print("llego")
    hola = request.POST.get('id')
    for key, value in request.POST.items():
        return Response(key+' '+value)

    for key, value in request.POST.items():
        reqenrol = Req_enrol.objects.get(enrolment_id=request.user.id,requirement_id=key)
        if reqenrol.state != 'V':
            print(request.user.id+" -> "+ key)
            reqenrol.update(state='P')

    return Response(status=200)