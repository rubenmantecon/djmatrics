from django.core.management.base import BaseCommand, CommandError
from core.models import *
# from core import factories

from datetime import datetime
import sys
import csv

# identificative strings for columns in CSV
CODI_ENSENYAMENT_ASSIGNAT_STR = "Codi ensenyament assignat"
REQ_NUM_STR = "Núm. sol·licitud"
RALC_ID = "Ident. RALC"

CODI_CENTRE = 8016781

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

        print("Carregant matrícules. Cada fila del fitxer es convertirà en una entrada a la taula Enrolments.")

        # stats
        no_admesos = 0
        no_admesos_centre = 0
        duplicats = 0
        admesos = 0
        errors = 0

        with open(filename) as f:
            reader = csv.DictReader(f, delimiter=",")
            for row in reader:
                # comprovar que l'alumne està admès al centre
                centre = row["Centre assignat"]
                if not centre or int(centre) != int(CODI_CENTRE):
                    no_admesos += 1
                    print("Alumne no admès a [{}]: {} {}, {}".format( centre,#CODI_CENTRE,
                            row["Primer cognom"], row["Segon cognom"], row["Nom"]
                        ))
                    continue

                # comprovar duplicats
                dup = Enrolment.objects.filter(request_num=row[REQ_NUM_STR]).first()
                if dup:
                    print("Matricula duplicada per a {} : {} {}, {}".format(
                        dup.request_num,dup.last_name_1,dup.last_name_2,dup.first_name))
                    duplicats += 1
                    continue

                career = Career.objects.filter(code=row[CODI_ENSENYAMENT_ASSIGNAT_STR]).first()
                if not career:
                    print("ERROR: No s'ha trobat estudis amb codi [ {} ] per a {}".format(
                                row[CODI_ENSENYAMENT_ASSIGNAT_STR], row[REQ_NUM_STR]))
                    errors += 1
                    # no guardem dades si no té cap estudi admès
                    #continue
                    # de moment ho creem igualment pq es vegi que no ha estat acceptat explícitament

                # CREATE ENROLMENT
                admesos += 1
                matricula = Enrolment(
                    request_num = row[REQ_NUM_STR],
                    ralc_num = row[RALC_ID],
                    first_name = row["Nom"],
                    last_name_1 = row["Primer cognom"],
                    last_name_2 = row["Segon cognom"],
                    career = career,
                    state = 'P', # pending
                )
                matricula.save()

        # stats
        print("No admesos: {}".format(no_admesos))
        print("Duplicats: {}".format(duplicats))
        print("Admesos: {}".format(admesos))
        print("Errors: {}".format(errors))
