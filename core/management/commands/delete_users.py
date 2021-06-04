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
        print("Esborrant els usuaris d'alumnes.")

        users = User.objects.filter(is_staff=False)
        n = users.count()

        users.delete()

        print("Usuaris d'alumnes eliminats: {}".format(n))
        
