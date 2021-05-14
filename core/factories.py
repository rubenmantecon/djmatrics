import factory
from factory import Factory,lazy_attribute
from faker import Faker
from factory.django import DjangoModelFactory
from core.models import User,Term, Career, MP, UF, Enrolment, Record, Requirement, Req_enrol, ProfileRequirement,EnrolmentUF, Upload

fake=Faker()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ()
    email = lazy_attribute(lambda x:  fake.language_name()+ "@"+fake.random_element(elements=('gmail', 'hotmail', 'outlook'))+ fake.random_element(elements=('.com', '.cat', '.es')))
    username = lazy_attribute(lambda x: fake.first_name()+fake.last_name()+"_student")
    password= factory.PostGenerationMethodCall('set_password','student')
    

class TermFactory(DjangoModelFactory):
    class Meta:
        model = Term
        django_get_or_create = ()

    name = lazy_attribute(lambda x: "Curs " +fake.year()+ "/"+fake.year())
    desc = lazy_attribute(lambda x: fake.paragraph())
    start = lazy_attribute(lambda x: fake.date_time_between(start_date='now', end_date='+10d', tzinfo=None))
    end = lazy_attribute(lambda x: fake.date_time_between(start_date='+11d', end_date='+30d', tzinfo=None))
    
class CareerFactory(DjangoModelFactory):
    class Meta:
        model = Career
        django_get_or_create = ()

    name = lazy_attribute(lambda x: fake.job())
    code = lazy_attribute(lambda x: fake.bothify(text='???##S', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    desc = lazy_attribute(lambda x: fake.catch_phrase())
    hours = lazy_attribute(lambda x: fake.random_number(digits=3, fix_len=True))
    start = lazy_attribute(lambda x: fake.date_time_between(start_date='now', end_date='+10d', tzinfo=None))
    end = lazy_attribute(lambda x: fake.date_time_between(start_date='+11d', end_date='+30d', tzinfo=None))
    term = factory.SubFactory(TermFactory)

class MpFactory(DjangoModelFactory):
    class Meta:
        model = MP
        django_get_or_create = ()
    name = lazy_attribute(lambda x: "MP " + fake.job())
    code = lazy_attribute(lambda x: fake.bothify(text='MP##'))
    desc = lazy_attribute(lambda x: fake.catch_phrase())
    career = factory.SubFactory(CareerFactory)

class UfFactory(DjangoModelFactory):
    class Meta:
        model = UF
        django_get_or_create = ()
    name = lazy_attribute(lambda x: "UF " + fake.job())
    code = lazy_attribute(lambda x: fake.bothify(text='UF##'))
    desc = lazy_attribute(lambda x: fake.catch_phrase())
    mp = factory.SubFactory(MpFactory)

class ProfileRequirementFactory(DjangoModelFactory):
    class Meta:
        model = ProfileRequirement
        django_get_or_create = ()
    name = lazy_attribute(lambda x: fake.safe_color_name())
    description = lazy_attribute(lambda x: fake.paragraph())
    profile_type = lazy_attribute(lambda x: fake.random_element(elements=('bonus', 'exemption')))
class EnrolmentFactory(DjangoModelFactory):
    class Meta:
        model = Enrolment
        django_get_or_create = ()
    role = factory.SubFactory(UserFactory)
    dni = lazy_attribute(lambda x: fake.bothify(text='########?', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    state = lazy_attribute(lambda x: fake.random_element(elements=('P', 'V', 'U')))
    birthplace = lazy_attribute(lambda x: fake.country())
    birthday = lazy_attribute(lambda x: fake.date_time_between(start_date='-18y', end_date='-17y', tzinfo=None))
    address = lazy_attribute(lambda x: fake.address())
    city = lazy_attribute(lambda x: fake.city())
    postal_code = lazy_attribute(lambda x: fake.bothify(text='#####'))
    phone_number = lazy_attribute(lambda x: fake.bothify(text='#########'))
    email = lazy_attribute(lambda x: fake.language_name()+ "@"+fake.random_element(elements=('gmail', 'hotmail', 'outlook'))+ fake.random_element(elements=('.com', '.cat', '.es')))
    emergency_number= lazy_attribute(lambda x: fake.bothify(text='#########'))
    tutor_1=lazy_attribute(lambda x: fake.name())
    tutor_2=lazy_attribute(lambda x: fake.name())
    tutor_1_dni=lazy_attribute(lambda x: fake.bothify(text='########?', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    tutor_2_dni=lazy_attribute(lambda x: fake.bothify(text='########?', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'))
    term = factory.SubFactory(TermFactory)
    career = factory.SubFactory(CareerFactory)
    excursions = lazy_attribute(lambda x: fake.random_element(elements=(1, 0)))
    extracurricular = lazy_attribute(lambda x: fake.random_element(elements=(1, 0)))
    image_rights = lazy_attribute(lambda x: fake.random_element(elements=(1, 0)))
    profile_req = factory.SubFactory(ProfileRequirementFactory)

class RecordFactory(DjangoModelFactory):
    class Meta:
        model = Record
        django_get_or_create = ()
    uf = factory.SubFactory(UfFactory)



class RequirementFactory(DjangoModelFactory):
    class Meta:
        model = Requirement
        django_get_or_create = ()
    name = lazy_attribute(lambda x: fake.random_element(elements=('DNI', 'Tarjeta Sanitaria', 'Tarjeta de familia numerosa')))
    profile = factory.SubFactory(ProfileRequirementFactory)
    
class Req_enrolFactory(DjangoModelFactory):
    class Meta:
        model = Req_enrol
        django_get_or_create = ()
    state = lazy_attribute(lambda x: fake.random_element(elements=('P', 'V', 'R','E')))
    requirement = factory.SubFactory(RequirementFactory)
    enrolment = factory.SubFactory(EnrolmentFactory)

class EnrolmentUFFactory(DjangoModelFactory):
    class Meta:
        model = EnrolmentUF
        django_get_or_create = ()
    uf = factory.SubFactory(UfFactory)
    enrolment = factory.SubFactory(EnrolmentFactory)
