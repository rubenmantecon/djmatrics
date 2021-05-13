from django.core.management.base import BaseCommand, CommandError
from core.models import *
#from core import factories

from datetime import datetime
import sys, csv

class Command(BaseCommand):
    help = """Importa cicles formatius.\n
    Sintaxi: python manage.py import_careers careers.csv
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

        print("Carregant cicles formatius. Es carregaran en un nou curs.")

        term_name = input("Nom del nou curs: ")
        term = Term(
                    name="[IMPORT] {}".format(term_name),
                    desc="Imported term",
                    start=datetime.today(),
                    active=True
            )
        term.save()

        last_career = None
        last_mp = None

        with open(filename) as f:
            reader = csv.DictReader(f,delimiter=";")
            for row in reader:
                codi_cicle = row["CODI_CICLE_FORMATIU"]
                nom_cicle = row["NOM_CICLE_FORMATIU"]
                hores_cicle = row["HORES_CICLE_FORMATIU"]
                codi_mp = row["CODI_MODUL"]
                nom_mp = row["NOM_MODUL"]
                codi_uf = row["CODI_UNITAT_FORMATIVA"]
                nom_uf = row["NOM_UNITAT_FORMATIVA"]

                # create career if doesn't exist
                # assumim que els MPs i UFs estan ordenats
                if not last_career or codi_cicle!=last_career.code:
                    print("Creant cicle: {}".format(nom_cicle))
                    career = Career(
                                name=nom_cicle,
                                code=codi_cicle,
                                hours=hores_cicle,
                                active=True,
                                term=term,
                                )
                    career.save()
                    last_career = career

                # create MP if doesn't exist
                if not last_mp or codi_mp!=last_mp.code:
                    #print("Creant MP: {}".format(nom_mp))
                    mp = MP(    name=nom_mp,
                                code=codi_mp,
                                career=last_career,)
                    mp.save()
                    last_mp = mp

                # create UF
                #print("Creant UF: {}".format(nom_uf))
                uf = UF(    name=nom_uf,
                            code=codi_uf,
                            mp=last_mp,)
                uf.save()


