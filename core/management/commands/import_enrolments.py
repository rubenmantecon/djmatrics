from django.core.management.base import BaseCommand, CommandError
from core.models import *
# from core import factories

from datetime import datetime
import sys
import csv


class Command(BaseCommand):
    help = """Importa matriculacions.\n
    Sintaxi: python manage.py import_enrolments <nom del fitxer>.csv
    """

    def add_arguments(self, parser):
        parser.add_argument('filename', nargs=1, type=str)

    def handle(self, *args, **options):
        filename = options["filename"][0]
        try:
            f = open(filename)
            f.close()
        except IOError:
            print('El fitxer "{}" no existeix'.format(filename))
            sys.exit()

        print("Carregant matrícules. Cada fila de matrícula del fitxer es convertirà en una entrada a la taula Enrolments.")

        with open(filename) as f:
            reader = csv.DictReader(f, delimiter=",")
            for row in reader:
                # Format the date coming from csv to DB's date format
                data_naixement = datetime.strptime(
                    row["Data naixement"], '%d/%m/%Y').strftime('%Y-%m-%d')
                matricula = Enrolment(
                    dni=row["DNI"], state="P", birthplace=row["País naixement"], birthday=data_naixement, address='{} {}, {}'.format(row["Tipus via"], row["Nom via"], row["Número via"]), city=row["Municipi residència"], postal_code=row["CP"], phone_number=row["Telèfon"], email=row["Correu electrònic"], emergency_number=row["Telèfon"], tutor_1_dni=row["Núm. doc. tutor 1"], tutor_2_dni=row["Núm. doc. tutor 2"], tutor_1_name=row["Nom tutor 1"], tutor_1_lastname1=row["Primer cognom tutor 1"], tutor_1_lastname2=row["Segon cognom tutor 1"], tutor_2_name=row["Nom tutor 2"], tutor_2_lastname1=row["Primer cognom tutor 2"], tutor_2_lastname2=row["Segon cognom tutor 2"]
                )
                matricula.save()