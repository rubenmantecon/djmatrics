from django.core.management.base import BaseCommand, CommandError
from core.models import *
# from core import factories

from datetime import datetime
import sys
import csv


class Command(BaseCommand):
    help = """Crea usuaris a partir de les matricules (enrolments).\n
    Sintaxi: python create_users
    """

    def handle(self, *args, **options):
        print("Creant usuaris a partir de la taula de Matriculacions (Enrolments).")

        # stats
        already_linked = 0
        not_found_email = 0
        already_created = 0
        created = 0

        for matricula in Enrolment.objects.all():
            if matricula.user:
                # enrolment already has a related user, skip
                already_linked += 1
                continue

            # check email
            if not matricula.email:
                print("Matricula sense email, no podrà logar-se al portal de matriculacions: {} {}, {} ".
                    format(matricula.last_name_1,matricula.last_name_2,matricula.first_name))
                not_found_email += 1
                continue

            # seek for already created user
            user = User.objects.filter(email=matricula.email).first()
            if user:
                # assign existing user and continue next enrolment
                matricula.user = user
                matricula.save()
                already_created += 1
                continue

            # create related user
            user = User(
                email = matricula.email,
                first_name = matricula.first_name,
                last_name = "{} {}".format(matricula.last_name_1,matricula.last_name_2),
                username = "{} {} {}".format(matricula.first_name,
                            matricula.last_name_1,matricula.last_name_2),
            )
            user.save()
            # link user to enrolment
            matricula.user = user
            matricula.save()
            created += 1

        # statistics summary
        print("Usuaris ja enllaçats: {}".format(already_linked))
        print("Matricules sense email: {}".format(not_found_email))
        print("Usuaris ja creats (possibles múltiples matricules si és el primer cop que executeu aquest script): {}".format(already_created))
        print("Usuaris creats: {}".format(created))
        
