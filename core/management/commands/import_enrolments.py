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
                    dni=row["DNI"], state=row["Estat sol·licitud"], birthplace=row["País naixement"], birthday=data_naixement, address='{} {}, {}'.format(row["Tipus via"], row["Nom via"], row["Número via"]), city=row["Municipi residència"], postal_code=row["CP"], phone_number=row["Telèfon"], email=row["Correu electrònic"], emergency_number=row["Telèfon"], tutor_1_dni=row["Núm. doc. tutor 1"], tutor_2_dni=row["Núm. doc. tutor 2"], tutor_1_name=row["Nom tutor 1"], tutor_1_lastname1=row["Primer cognom tutor 1"], tutor_1_lastname2=row["Segon cognom tutor 1"], tutor_2_name=row["Nom tutor 2"], tutor_2_lastname1=row["Primer cognom tutor 2"], tutor_2_lastname2=row["Segon cognom tutor 2"]
                )
                matricula.save()

                """
                any_escolar = row["Convocatòria"]
                codi_solicitud= row["Codi sol·licitud"]
                tipus_solicitud = row["Tipus"]
                estat_solicitud = row["Estat sol·licitud"]
                nom_alumne = row["Nom"]
                cognom1_alumne = row["Primer cognom"]
                cognom2_alumne = row["Segon cognom"]
                ralc_id = row["Identificació RALC"]
                tipus_alumne = row["Tipus Alumne"]
                codi_centre_p1 = row["Codi centre P1"]
                nom_centre_p1 = row["Nom centre P1"]
                naturalesa_centre_p1 = row["Naturalesa centre P1"]
                municipi_centre_p1 = row["Municipi centre P1"]
                sttt_centr_p1 = row["SSTT centre P1"]
                codi_ensenyament_p1 = row["Codi ensenyament P1"]
                nom_ensenyament_p1 = row["Nom ensenyament P1"]
                codi_modalitat = row["Codi modalitat"]
                modalitat = row["Codi modalitat"]
                curs_p1 = row["Curs P1"]
                regim_p1 = row["Règim P1"]
                torn_p1 = row["Règim P1"]
                dni = row["DNI"]
                nie = row["nie"]
                password = row["PASS"]
                tis = row["TIS"]
                data_naixement = row["Data naixement"]
                z = row["z"]
                nacionalitat = row["Nacionalitat"]
                pais_naixement = row["País naixement"]
                municipi_naixement = row["Municipi naixement"]
                tipus_via = row["Tipus via"]
                nom_via = row["Nom via"]
                """
