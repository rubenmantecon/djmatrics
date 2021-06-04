from django.core.management.base import BaseCommand, CommandError
from core.models import *
# from core import factories

from datetime import datetime
import sys
import csv


# identificative strings for columns in CSV
CODI_ENSENYAMENT_ASSIGNAT_STR = "Codi ensenyament assignat"
REQ_NUM_STR = "Codi sol·licitud"
RALC_ID = "Ident. RALC"


class Command(BaseCommand):
    help = """Importa dades personals.\n
    Sintaxi: python manage.py import_personal_data <nom del fitxer>.csv
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

        print("Carregant dades personals. Només s'importaran les dades de les persones presents a la taula Enrolments.")

        with open(filename) as f:
            reader = csv.DictReader(f, delimiter=",")
            for row in reader:
                # busquem objecte relacionat
                matricula = Enrolment.objects.filter(
                                request_num=row[REQ_NUM_STR])

                if matricula.count() == 0:
                    print("Matricula no trobada (skipped): {} - {} {} {} ".format(
                            row["DNI"], row["Nom"], row["Primer cognom"], row["Segon cognom"]))
                    # avancem al seguent element de la llista
                    continue

                matricula = matricula.first()

                # ID CARD
                ID_num = None
                ID_type = None # ID_type as indicated in model.Enrolment
                if row["DNI"]:
                    ID_type = "DNI"
                    ID_num = row["DNI"]
                elif row["NIE"]:
                    ID_type = "NIE"
                    ID_num = row["NIE"]
                elif row["PASS"]:
                    ID_type = "PASS"
                    ID_num = row["PASS"]
                else:
                    print("Document no trobat per a {} {} {}".format(
                        row["Nom"], row["Primer cognom"], row["Segon cognom"]))
                    # si no trobem ID, no importem dades
                    continue

                # Format the date coming from csv to DB's date format
                data_naixement = datetime.strptime(
                    row["Data naixement"], '%d/%m/%Y').strftime('%Y-%m-%d')

                matricula.first_name = row["Nom"]
                matricula.last_name_1 = row["Primer cognom"]
                matricula.last_name_2 = row["Segon cognom"]
                matricula.ID_num = ID_num
                matricula.ID_type = ID_type
                matricula.tis = row["TIS"]
                matricula.state = "P"
                matricula.birthplace = row["País naixement"]
                matricula.birthday = data_naixement
                matricula.address = '{} {}, {}'.format(row["Tipus via"],
                                     row["Nom via"], row["Número via"])
                matricula.city = row["Municipi residència"]
                matricula.postal_code = row["CP"]
                matricula.phone_number = row["Telèfon"]
                matricula.email = row["Correu electrònic"]
                matricula.emergency_number = row["Telèfon"]
                matricula.tutor_1_dni = row["Núm. doc. tutor 1"]
                matricula.tutor_2_dni = row["Núm. doc. tutor 2"]
                matricula.tutor_1_name = row["Nom tutor 1"]
                matricula.tutor_1_lastname1 = row["Primer cognom tutor 1"]
                matricula.tutor_1_lastname2 = row["Segon cognom tutor 1"]
                matricula.tutor_2_name = row["Nom tutor 2"]
                matricula.tutor_2_lastname1 = row["Primer cognom tutor 2"]
                matricula.tutor_2_lastname2 = row["Segon cognom tutor 2"]

                # update matricula info
                matricula.save()

