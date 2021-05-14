import random
from django.db import transaction
from django.core.management.base import BaseCommand
from core.models import User,Term, Career, MP, UF, Enrolment, Record, Requirement, Req_enrol, ProfileRequirement,EnrolmentUF, Upload
from core.factories import (
    UserFactory,
    TermFactory,
    CareerFactory,
    MpFactory,
    UfFactory,
    EnrolmentFactory,
    RecordFactory,
    ProfileRequirementFactory,
    RequirementFactory,
    Req_enrolFactory,
    EnrolmentUFFactory
)

REGISTERS = 10



class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [User,Term,Career,MP,UF,Enrolment,Record,ProfileRequirement,Requirement,Req_enrol,EnrolmentUF]
        #for m in models:
            #m.objects.all().delete()

        self.stdout.write("Creating new data...")
        
        for _ in range(REGISTERS):
            #Another iteration is needed in order to add real information to: requirements, profile requirements...
            user= UserFactory()
            term = TermFactory()
            career = CareerFactory()
            mp=MpFactory()
            uf=UfFactory()
            profilerequirement=ProfileRequirementFactory()
            enrolment=EnrolmentFactory()
            record = RecordFactory()
            requirement=RequirementFactory()
            req_enrol=Req_enrolFactory()
            enrolmentUF=EnrolmentUFFactory()
